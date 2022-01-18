"""Convert substrait things into ibis things.

The primary API here is :func:`decompile`.
"""

from __future__ import annotations

import collections
import datetime
import functools
import operator
import uuid
from typing import Any, Callable, Deque, Hashable, Sequence, TypeVar

import ibis
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.schema as sch
import ibis.expr.types as ir
import inflection
import pytz
import toolz

from ..proto.substrait import expression_pb2 as stexpr
from ..proto.substrait import plan_pb2 as stp
from ..proto.substrait import relations_pb2 as strel
from ..proto.substrait import type_pb2 as stt
from .core import SubstraitDecompiler, _get_fields, which_one_of
from .translate import _MICROSECONDS_PER_SECOND, _MINUTES_PER_HOUR, _SECONDS_PER_MINUTE

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

_DEFAULT_TIMEZONE = pytz.utc
_DEFAULT_TIMEZONE_STRING = _DEFAULT_TIMEZONE.zone


@functools.singledispatch
def _decompile_type(typ: Any, *args: Any, **kwargs: Any) -> dt.DataType:
    raise NotImplementedError(
        f"decompilation of substrait type(s) `{tuple(type(t).__name__ for t in args)}`"
        " to an ibis type is not yet implemented"
    )


def _decompile_nullability(typ: Any) -> bool:
    nullability = typ.nullability
    if nullability in (
        stt.Type.Nullability.NULLABILITY_NULLABLE,
        stt.Type.Nullability.NULLABILITY_UNSPECIFIED,
    ):
        return True
    elif nullability == stt.Type.Nullability.NULLABILITY_REQUIRED:
        return False
    raise ValueError(
        f"Unknown TypeNullability variant: {stt.Type.Nullability.Name(nullability)}"
    )


@_decompile_type.register
def _decompile_type_type(typ: stt.Type) -> dt.DataType:
    _, kind = which_one_of(typ, "kind")
    return _decompile_type(kind, _decompile_nullability(kind))


@_decompile_type.register
def _decompile_type_boolean(typ: stt.Type.Boolean, nullable: bool) -> dt.DataType:
    return dt.Boolean(nullable=nullable)


@_decompile_type.register
def _decompile_type_i8(typ: stt.Type.I8, nullable: bool) -> dt.DataType:
    return dt.Int8(nullable=nullable)


@_decompile_type.register
def _decompile_type_i16(typ: stt.Type.I16, nullable: bool) -> dt.DataType:
    return dt.Int16(nullable=nullable)


@_decompile_type.register
def _decompile_type_i32(typ: stt.Type.I32, nullable: bool) -> dt.DataType:
    return dt.Int32(nullable=nullable)


@_decompile_type.register
def _decompile_type_i64(typ: stt.Type.I64, nullable: bool) -> dt.DataType:
    return dt.Int64(nullable=nullable)


@_decompile_type.register
def _decompile_type_fp32(typ: stt.Type.FP32, nullable: bool) -> dt.DataType:
    return dt.Float32(nullable=nullable)


@_decompile_type.register
def _decompile_type_fp64(typ: stt.Type.FP64, nullable: bool) -> dt.DataType:
    return dt.Float64(nullable=nullable)


@_decompile_type.register(stt.Type.String)
@_decompile_type.register(stt.Type.VarChar)
@_decompile_type.register(stt.Type.FixedChar)
def _decompile_type_string(
    typ: stt.Type.String | stt.Type.VarChar | stt.Type.FixedChar,
    nullable: bool,
) -> dt.DataType:
    return dt.String(nullable=nullable)


@_decompile_type.register(stt.Type.Binary)
@_decompile_type.register(stt.Type.FixedBinary)
def _decompile_type_binary(
    typ: stt.Type.Binary | stt.Type.FixedBinary,
    nullable: bool,
) -> dt.DataType:
    return dt.Binary(nullable=nullable)


@_decompile_type.register
def _decompile_type_date(typ: stt.Type.Date, nullable: bool) -> dt.DataType:
    return dt.Date(nullable=nullable)


@_decompile_type.register
def _decompile_type_timestamp(typ: stt.Type.Timestamp, nullable: bool) -> dt.DataType:
    return dt.Timestamp(nullable=nullable)


@_decompile_type.register
def _decompile_type_timestamp_tz(
    typ: stt.Type.TimestampTZ,
    nullable: bool,
) -> dt.DataType:
    return dt.Timestamp(_DEFAULT_TIMEZONE_STRING, nullable=nullable)


@_decompile_type.register
def _decompile_type_time(typ: stt.Type.Time, nullable: bool) -> dt.DataType:
    return dt.Time(nullable=nullable)


@_decompile_type.register
def _decompile_type_decimal(typ: stt.Type.Decimal, nullable: bool) -> dt.DataType:
    return dt.Decimal(
        precision=typ.precision,
        scale=typ.scale,
        nullable=nullable,
    )


@_decompile_type.register
def _decompile_type_uuid(typ: stt.Type.UUID, nullable: bool) -> dt.DataType:
    return dt.UUID(nullable=nullable)


@_decompile_type.register
def _decompile_type_list(typ: stt.Type.List, nullable: bool) -> dt.DataType:
    return dt.Array(_decompile_type(typ.type), nullable=nullable)


@_decompile_type.register
def _decompile_type_map(typ: stt.Type.Map, nullable: bool) -> dt.DataType:
    return dt.Map(
        _decompile_type(typ.key),
        _decompile_type(typ.value),
        nullable=nullable,
    )


@functools.singledispatch
def _decompile_field(typ: Any, names: Deque[str], *args: Any) -> dt.DataType:
    raise NotImplementedError(f"unknown field type when decompiling: {type(typ)}")


@_decompile_field.register
def _decompile_field_generic(
    typ: stt.Type,
    names: Deque[str],
) -> dt.DataType:
    _, kind = which_one_of(typ, "kind")
    return _decompile_field(kind, names, _decompile_nullability(kind))


@_decompile_field.register(stt.Type.Boolean)
@_decompile_field.register(stt.Type.I8)
@_decompile_field.register(stt.Type.I16)
@_decompile_field.register(stt.Type.I32)
@_decompile_field.register(stt.Type.I64)
@_decompile_field.register(stt.Type.FP64)
@_decompile_field.register(stt.Type.FP32)
@_decompile_field.register(stt.Type.String)
@_decompile_field.register(stt.Type.Binary)
@_decompile_field.register(stt.Type.Timestamp)
@_decompile_field.register(stt.Type.Date)
@_decompile_field.register(stt.Type.Time)
@_decompile_field.register(stt.Type.UUID)
@_decompile_field.register(stt.Type.Decimal)
def _decompile_field_primitive(typ: Any, _: Deque[str], nullable: bool) -> dt.DataType:
    return _decompile_type(typ, nullable)


@_decompile_field.register
def _decompile_field_array(
    typ: stt.Type.List,
    names: Deque[str],
    nullable: bool,
) -> dt.DataType:
    return dt.Array(
        value_type=_decompile_field(typ.type, names),
        nullable=nullable,
    )


@_decompile_field.register
def _decompile_field_map(
    typ: stt.Type.Map,
    names: Deque[str],
    nullable: bool,
) -> dt.DataType:
    return dt.Map(
        key_type=_decompile_field(typ.key, names),
        value_type=_decompile_field(typ.value, names),
        nullable=nullable,
    )


def _decompile_struct_fields(
    typ: stt.Type.Struct,
    names: Deque[str],
) -> list[tuple[str, dt.DataType]]:
    fields = []

    for ftype in typ.types:
        name = names.popleft()
        field = _decompile_field(ftype, names)
        fields.append((name, field))

    return fields


@_decompile_field.register
def _st_to_ibis_struct(
    typ: stt.Type.Struct,
    names: Deque[str],
    nullable: bool,
) -> dt.DataType:
    fields = _decompile_struct_fields(typ, names)
    return dt.Struct.from_tuples(fields, nullable=_decompile_nullability(typ))


@functools.singledispatch
def decompile_schema(obj: Any) -> sch.Schema:
    raise NotImplementedError(f"decompile_schema for {type(obj)} not implemented")


@decompile_schema.register
def _decompile_schema_named_struct(schema: stt.NamedStruct) -> sch.Schema:
    """Turn a Substrait ``TypeNamedStruct`` into an ibis schema."""
    names_queue = collections.deque(schema.names)
    name_type_pairs = _decompile_struct_fields(schema.struct, names_queue)
    if names_queue:
        raise ValueError(
            "field names remaining when decompiling Substrait schema: "
            f"{list(names_queue)}"
        )
    return sch.Schema.from_tuples(name_type_pairs)


@decompile_schema.register
def _decompile_schema_rel(rel: strel.Rel) -> sch.Schema:
    _, variant = which_one_of(rel, "rel_type")
    return decompile_schema(variant)


@decompile_schema.register
def _decompile_schema_type_named_struct(read_rel: strel.ReadRel) -> sch.Schema:
    """Turn a Substrait ``TypeNamedStruct`` into an ibis schema."""
    return decompile_schema(read_rel.base_schema)


@decompile_schema.register(strel.FilterRel)
@decompile_schema.register(strel.FetchRel)
@decompile_schema.register(strel.SortRel)
def _decompile_schema_remaining_rels(
    rel: strel.FilterRel | strel.FetchRel | strel.SortRel,
) -> sch.Schema:
    return decompile_schema(rel.input)


@functools.singledispatch
def decompile(msg: Any, *args: Any) -> ir.Expr:
    """Construct an ibis expression from a substrait `Rel`."""
    raise NotImplementedError(
        f"decompiling substrait IR type `{type(msg).__name__}` to an ibis "
        "expression is not yet implemented"
    )


@decompile.register(stp.Plan)
def _decompile_plan(plan: stp.Plan) -> list[ir.TableExpr]:
    decompiler = SubstraitDecompiler(plan)
    return [decompile(relation, decompiler) for relation in plan.relations]


@decompile.register
def _decompile_plan_rel(
    rel: stp.PlanRel,
    decompiler: SubstraitDecompiler,
) -> ir.TableExpr:
    rel_variant_name, rel_variant = which_one_of(rel, "rel_type")
    return decompile(rel_variant, decompiler)


def _rename_schema(schema: ibis.Schema, names: Sequence[str]) -> ibis.Schema:
    from .translate import translate

    named_struct = translate(schema)
    return decompile_schema(stt.NamedStruct(names=names, struct=named_struct.struct))


@decompile.register
def _decompile_rel_root(
    rel_root: strel.RelRoot,
    decompiler: SubstraitDecompiler,
) -> ir.TableExpr:
    return decompile(rel_root.input, decompiler, collections.deque(rel_root.names))


@decompile.register
def _decompile_rel(
    rel: strel.Rel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    _, rel_variant = which_one_of(rel, "rel_type")
    return decompile(rel_variant, decompiler, names)


@decompile.register
def _decompile_read_rel(
    read_rel: strel.ReadRel,
    decompiler: SubstraitDecompiler,
    _names: Deque[str],
) -> ir.TableExpr:
    _, read_rel_variant = which_one_of(read_rel, "read_type")
    schema = decompile_schema(read_rel)
    return decompile(read_rel_variant, schema, decompiler)


@decompile.register
def _decompile_named_table(
    named_table: strel.ReadRel.NamedTable,
    schema: ibis.Schema,
    decompiler: SubstraitDecompiler,
) -> ir.TableExpr:
    names = named_table.names
    if not names:
        raise ValueError(f"no table names found when consuming {named_table}")
    try:
        (name,) = names
    except ValueError as e:
        raise ValueError("more than one named table not supported") from e

    # TODO: replace with ops.CatalogTable once there's an ibis client impl
    return ibis.table(schema=schema, name=name)


def _get_child_tables(child: ir.TableExpr) -> Sequence[ops.TableNode]:
    child_op = child.op()
    if isinstance(child_op, ops.Join):
        return [child_op.left, child_op.right]
    return [child]


@decompile.register
def _decompile_filter_rel(
    filter_rel: strel.FilterRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(filter_rel.input, decompiler, names)
    predicate = decompile(filter_rel.condition, _get_child_tables(child), decompiler)
    return child.filter(predicate)


@decompile.register
def _decompile_fetch_rel(
    fetch_rel: strel.FetchRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(fetch_rel.input, decompiler, names)
    return child.limit(fetch_rel.count, offset=fetch_rel.offset)


_JOIN_METHOD_TABLE = {
    strel.JoinRel.JoinType.JOIN_TYPE_INNER: "inner",
    strel.JoinRel.JoinType.JOIN_TYPE_OUTER: "outer",
    strel.JoinRel.JoinType.JOIN_TYPE_LEFT: "left",
    strel.JoinRel.JoinType.JOIN_TYPE_RIGHT: "right",
    strel.JoinRel.JoinType.JOIN_TYPE_SEMI: "semi",
    strel.JoinRel.JoinType.JOIN_TYPE_ANTI: "anti",
}


@decompile.register
def _decompile_join_rel(
    join_rel: strel.JoinRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    left_child = decompile(join_rel.left, decompiler, names)
    right_child = decompile(join_rel.right, decompiler, names)
    join_method_name = _JOIN_METHOD_TABLE[join_rel.type]
    predicates = decompile(join_rel.expression, [left_child, right_child], decompiler)
    join_method = getattr(left_child, f"{join_method_name}_join")
    # TODO: implement post_join_filter
    return join_method(right_child, predicates=predicates)


@decompile.register
def _decompile_sort_rel(
    sort_rel: strel.SortRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(sort_rel.input, decompiler, names)
    children = _get_child_tables(child)
    sorts = [decompile(sort, children, decompiler) for sort in sort_rel.sorts]
    return child.sort_by(sorts)


def _remove_names_below(names: Deque[str], dtype: dt.DataType) -> None:
    """Remove all levels of `names` below the names in `dtype`.

    Examples
    --------
    >>> from collections import deque
    >>> import ibis
    >>> import ibis.expr.datatypes as dt
    >>> typestr = "struct<b: struct<c: int64, d: struct<e: float64>>>"
    >>> schema = ibis.schema([("a", typestr), ("f", "string")])
    >>> dtype = dt.parse_type(typestr)
    >>> flat_names = deque(["a", "b", "c", "d", "e", "f"])
    >>> field_name = flat_names.popleft()
    >>> _remove_names_below(flat_names, dtype)
    >>> flat_names
    deque(['f'])

    >>> flat_names = deque(["a", "b", "c", "d", "e", "f"])
    >>> _remove_names_below(flat_names, dtype)
    Traceback (most recent call last):
      ...
    ValueError: expected name `b`, got `a`; names: deque(['b', 'c', 'd', 'e', 'f'])
    """
    fields = list(_get_fields(dtype))

    while fields:
        name, typ = fields.pop()

        # arrays and and maps aren't named so we use None as a placeholder to
        # ensure that we traverse down their embedded types
        if name is not None:
            popped_name = names.popleft()
            if name != popped_name:
                raise ValueError(
                    f"expected name `{name}`, got `{popped_name}`; names: {names}"
                )

        fields.extend(_get_fields(typ))


def _decompile_with_name(
    expr: stexpr.Expression | stexpr.AggregateFunction,
    children: Sequence[ir.TableExpr],
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.ValueExpr:
    ibis_expr = decompile(expr, children, decompiler).name(names.popleft())

    # remove child names since those are encoded in the data type
    _remove_names_below(names, ibis_expr.type())

    return ibis_expr


@decompile.register
def _decompile_project_rel(
    project_rel: strel.ProjectRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(project_rel.input, decompiler, names)
    children = _get_child_tables(child)
    exprs = [
        _decompile_with_name(expr, children, decompiler, names)
        for expr in project_rel.expressions
    ]

    return child.projection(exprs)


@decompile.register
def _decompile_aggregate_rel(
    aggregate_rel: strel.AggregateRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    # TODO: aggregate_rel.phase is ignored, do we need to preserve it?
    child = decompile(aggregate_rel.input, decompiler, names)
    children = _get_child_tables(child)

    # TODO: only a single grouping set is allowed, implement grouping sets in
    # ibis upstream
    by: list[ir.ValueExpr] = []

    for grouping_expressions in map(
        operator.attrgetter("grouping_expressions"),
        aggregate_rel.groupings,
    ):
        if grouping_expressions and len(grouping_expressions) > 1:
            raise NotImplementedError(
                "more than one field per grouping is not yet implemented"
            )
        by.extend(
            _decompile_with_name(grouping_expression, children, decompiler, names)
            for grouping_expression in grouping_expressions
        )

    metrics = [
        _decompile_with_name(agg_rel_measure.measure, children, decompiler, names)
        for agg_rel_measure in aggregate_rel.measures
    ]

    return child.aggregate(by=by, metrics=metrics)


@decompile.register
def _decompile_expression_aggregate_function(
    aggregate_function: stexpr.AggregateFunction,
    children: Sequence[ir.TableExpr],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    extension = decompiler.function_extensions[aggregate_function.function_reference]
    function_name = extension.name
    op_type = getattr(ops, inflection.camelize(function_name))
    args = [decompile(arg, children, decompiler) for arg in aggregate_function.args]

    # XXX: handle table.count(); what an annoying hack
    if not args and issubclass(op_type, ops.Count):
        args += tuple(children)

    expr = op_type(*args).to_expr()
    output_type = _decompile_type(aggregate_function.output_type)
    if expr.type() != output_type:
        return expr.cast(output_type)
    return expr


class SetOpDecompiler:
    @staticmethod
    def decompile_SET_OP_MINUS_PRIMARY(
        left: ir.TableExpr,
        right: ir.TableExpr,
    ) -> ir.TableExpr:
        return left.difference(right)

    @staticmethod
    def decompile_SET_OP_INTERSECTION_PRIMARY(
        left: ir.TableExpr,
        right: ir.TableExpr,
    ) -> ir.TableExpr:
        return left.intersect(right)

    @staticmethod
    def decompile_SET_OP_UNION_DISTINCT(
        left: ir.TableExpr,
        right: ir.TableExpr,
    ) -> ir.TableExpr:
        return left.union(right, distinct=True)

    @staticmethod
    def decompile_SET_OP_UNION_ALL(
        left: ir.TableExpr,
        right: ir.TableExpr,
    ) -> ir.TableExpr:
        return left.union(right, distinct=False)


def _decompile_set_op(
    left: strel.Rel,
    right: strel.Rel,
    *,
    op: strel.SetRel.SetOp.V,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    left_expr = decompile(left, decompiler, names)
    right_expr = decompile(right, decompiler, names)
    name = strel.SetRel.SetOp.Name(op)
    method = getattr(SetOpDecompiler, f"decompile_{name}", None)
    if method is None:
        raise NotImplementedError(f"set operation not yet implemented: `{name}`")
    return method(left_expr, right_expr)


@decompile.register
def _decompile_set_op_rel(
    set_rel: strel.SetRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    return functools.reduce(
        functools.partial(
            _decompile_set_op,
            op=set_rel.op,
            decompiler=decompiler,
            names=names,
        ),
        set_rel.inputs,
    )


class ExpressionDecompiler:
    @staticmethod
    def decompile_literal(
        literal: stexpr.Expression.Literal,
        _children: Sequence[ir.TableExpr],
        _decompiler: SubstraitDecompiler,
    ) -> ir.ScalarExpr:
        value, dtype = decompile(literal)
        return ibis.literal(value, type=dtype)

    @staticmethod
    def decompile_selection(
        ref: stexpr.Expression.FieldReference,
        children: Sequence[ir.TableExpr],
        _: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        ref_type, ref_variant = which_one_of(ref, "reference_type")
        if ref_type != "direct_reference":
            raise NotImplementedError(
                f"decompilation of `{ref_type}` references are not yet implemented"
            )

        assert isinstance(ref_variant, stexpr.Expression.ReferenceSegment)

        direct_ref_type, direct_ref_variant = which_one_of(
            ref_variant,
            "reference_type",
        )
        assert isinstance(
            direct_ref_variant,
            stexpr.Expression.ReferenceSegment.StructField,
        )
        field_index = direct_ref_variant.field

        # this is zero if not set, which coincides nicely with the length 1 of
        # children in the case of no join; otherwise this value is the
        # zero-based index of the relation involved in the join
        child_relation_index = direct_ref_variant.child.struct_field.field
        # get the child relation, commonly zeroth, but could be first in the
        # case of a join
        child = children[child_relation_index]
        # return the field of the child
        return child[field_index]

    @staticmethod
    def decompile_scalar_function(
        scalar_func: stexpr.Expression.ScalarFunction,
        children: Sequence[ir.TableExpr],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return decompile(scalar_func, children, decompiler)


@decompile.register
def _decompile_expression(
    msg: stexpr.Expression,
    children: Sequence[ir.TableExpr],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    rex_type_name, rex = which_one_of(msg, "rex_type")
    method = getattr(ExpressionDecompiler, f"decompile_{rex_type_name}", None)
    if method is None:
        raise NotImplementedError(
            f"decompilation of {rex_type_name!r} expression variant not implemented"
        )
    return method(rex, children, decompiler)


@decompile.register
def _decompile_expression_scalar_function(
    msg: stexpr.Expression.ScalarFunction,
    children: Sequence[ir.TableExpr],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    extension = decompiler.function_extensions[msg.function_reference]
    function_name = extension.name
    op_type = getattr(ops, inflection.camelize(function_name))
    expr = op_type(
        *(decompile(arg, children, decompiler) for arg in msg.args)
    ).to_expr()
    output_type = _decompile_type(msg.output_type)
    if expr.type() != output_type:
        return expr.cast(output_type)
    return expr


@decompile.register
def _decompile_expression_sort_field(
    msg: stexpr.SortField,
    children: Sequence[ir.TableExpr],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    expr = decompile(msg.expr, children, decompiler)
    sort_field_func = _decompile_sort_field_type(msg.direction)
    return sort_field_func(expr)


def _decompile_sort_field_type(
    sort_type: stexpr.SortField.SortDirection.V,
) -> Callable[[T], Any]:
    if sort_type in {
        stexpr.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_FIRST,
        stexpr.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_LAST,
    }:
        return toolz.identity
    elif sort_type in {
        stexpr.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_FIRST,
        stexpr.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_LAST,
    }:
        return ibis.desc
    else:
        raise NotImplementedError(f"unknown sort type when decompiling: `{sort_type}`")


class LiteralDecompiler:
    @staticmethod
    def decompile_boolean(value: bool) -> tuple[bool, dt.Boolean]:
        return value, dt.boolean

    @staticmethod
    def decompile_i8(value: int) -> tuple[int, dt.Int8]:
        return value, dt.int8

    @staticmethod
    def decompile_i16(value: int) -> tuple[int, dt.Int16]:
        return value, dt.int16

    @staticmethod
    def decompile_i32(value: int) -> tuple[int, dt.Int32]:
        return value, dt.int32

    @staticmethod
    def decompile_i64(value: int) -> tuple[int, dt.Int64]:
        return value, dt.int64

    @staticmethod
    def decompile_fp32(value: float) -> tuple[float, dt.Float32]:
        return value, dt.float32

    @staticmethod
    def decompile_fp64(value: float) -> tuple[float, dt.Float64]:
        return value, dt.float64

    @staticmethod
    def decompile_timestamp(value: int) -> tuple[datetime.datetime, dt.Timestamp]:
        return (
            datetime.datetime.fromtimestamp(value / _MICROSECONDS_PER_SECOND),
            dt.timestamp,
        )

    @staticmethod
    def decompile_date(value: int) -> tuple[datetime.date, dt.Date]:
        timestamp = datetime.datetime.utcfromtimestamp(0) + datetime.timedelta(
            days=value
        )
        return timestamp.date(), dt.date

    @staticmethod
    def decompile_list(
        value: stexpr.Expression.Literal.List,
    ) -> tuple[list[T], dt.Array]:
        assert value.values, "Empty list found, expected non-empty list"
        values, types = zip(*map(decompile, value.values))
        return list(values), dt.Array(dt.highest_precedence(types))

    @staticmethod
    def decompile_empty_list(typ: stt.Type.List) -> tuple[list[T], dt.Array]:
        return [], _decompile_type(typ, nullable=True)

    @staticmethod
    def decompile_null(type: stt.Type) -> tuple[None, dt.DataType]:
        _, value = which_one_of(type, "kind")
        return None, _decompile_type(value, nullable=True)

    @staticmethod
    def decompile_binary(value: bytes) -> tuple[bytes, dt.Binary]:
        return value, dt.binary

    @staticmethod
    def decompile_string(value: str) -> tuple[str, dt.String]:
        return value, dt.string

    @staticmethod
    def decompile_uuid(value: bytes) -> tuple[uuid.UUID, dt.UUID]:
        return uuid.UUID(bytes=value), dt.uuid

    @staticmethod
    def decompile_timestamp_tz(value: int) -> tuple[datetime.datetime, dt.Timestamp]:
        return (
            datetime.datetime.fromtimestamp(
                value / _MICROSECONDS_PER_SECOND,
                tz=_DEFAULT_TIMEZONE,
            ),
            dt.Timestamp(timezone=_DEFAULT_TIMEZONE_STRING),
        )

    @staticmethod
    def decompile_time(value: int) -> tuple[datetime.time, dt.Time]:
        return _time_from_micros(value), dt.time

    @staticmethod
    def decompile_map(
        value: stexpr.Expression.Literal.Map,
    ) -> tuple[dict[K, V], dt.Map]:
        result = {}

        key_types = []
        value_types = []

        for key_value in value.key_values:
            key, key_type = decompile(key_value.key)
            key_types.append(key_type)

            result[key], value_type = decompile(key_value.value)
            value_types.append(value_type)

        return result, dt.Map(
            dt.highest_precedence(key_types),
            dt.highest_precedence(value_types),
        )

    @staticmethod
    def decompile_empty_map(typ: stt.Type.Map) -> tuple[dict[K, V], dt.Map]:
        return {}, _decompile_type(typ, nullable=True)


def _time_from_micros(value: int) -> datetime.time:
    """Convert microseconds since start-of-day to a :class:`datetime.time`."""
    microsecond = value % _MICROSECONDS_PER_SECOND
    second = (value // _MICROSECONDS_PER_SECOND) % _SECONDS_PER_MINUTE
    minute = (
        value // (_MICROSECONDS_PER_SECOND * _SECONDS_PER_MINUTE)
    ) % _MINUTES_PER_HOUR
    hour = value // (_MICROSECONDS_PER_SECOND * _SECONDS_PER_MINUTE * _MINUTES_PER_HOUR)
    return datetime.time(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
    )


@decompile.register(stexpr.Expression.Literal)
def _decompile_literal(msg: stexpr.Expression.Literal) -> tuple[T, dt.DataType]:
    literal_type_name, literal = which_one_of(msg, "literal_type")
    method = getattr(LiteralDecompiler, f"decompile_{literal_type_name}", None)
    if method is None:
        raise NotImplementedError(
            f"decompilation of `{literal_type_name}` literals not yet implemented"
        )
    return method(literal)
