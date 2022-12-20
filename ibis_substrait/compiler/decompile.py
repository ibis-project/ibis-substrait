"""Convert substrait things into ibis things.

The primary API here is :func:`decompile`.
"""

from __future__ import annotations

import bisect
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
import pytz
import toolz

from ibis_substrait.compiler.core import SubstraitDecompiler, _get_fields, which_one_of
from ibis_substrait.compiler.mapping import SUBSTRAIT_IBIS_OP_MAPPING
from ibis_substrait.compiler.translate import (
    _MICROSECONDS_PER_SECOND,
    _MINUTES_PER_HOUR,
    _SECONDS_PER_MINUTE,
)
from ibis_substrait.proto.substrait.ibis import algebra_pb2 as stalg
from ibis_substrait.proto.substrait.ibis import plan_pb2 as stp
from ibis_substrait.proto.substrait.ibis import type_pb2 as stt

try:
    from ibis.expr.operations import CountStar

    del CountStar
except ImportError:
    ops.CountStar = ops.Count

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
@_decompile_field.register(stt.Type.VarChar)
@_decompile_field.register(stt.Type.FixedChar)
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
def _decompile_schema_rel(rel: stalg.Rel) -> sch.Schema:
    _, variant = which_one_of(rel, "rel_type")
    return decompile_schema(variant)


@decompile_schema.register
def _decompile_schema_type_named_struct(read_rel: stalg.ReadRel) -> sch.Schema:
    """Turn a Substrait ``TypeNamedStruct`` into an ibis schema."""
    return decompile_schema(read_rel.base_schema)


@decompile_schema.register(stalg.FilterRel)
@decompile_schema.register(stalg.FetchRel)
@decompile_schema.register(stalg.SortRel)
def _decompile_schema_remaining_rels(
    rel: stalg.FilterRel | stalg.FetchRel | stalg.SortRel,
) -> sch.Schema:
    return decompile_schema(rel.input)


@functools.singledispatch
def decompile(msg: Any, *args: Any, **kwargs: Any) -> ir.Expr:
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
    rel_root: stalg.RelRoot,
    decompiler: SubstraitDecompiler,
) -> ir.TableExpr:
    return decompile(rel_root.input, decompiler, collections.deque(rel_root.names))


@decompile.register
def _decompile_rel(
    rel: stalg.Rel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    _, rel_variant = which_one_of(rel, "rel_type")
    return decompile(rel_variant, decompiler, names)


@decompile.register
def _decompile_read_rel(
    read_rel: stalg.ReadRel,
    decompiler: SubstraitDecompiler,
    _names: Deque[str],
) -> ir.TableExpr:
    _, read_rel_variant = which_one_of(read_rel, "read_type")
    schema = decompile_schema(read_rel)
    return decompile(read_rel_variant, schema, decompiler)


@decompile.register
def _decompile_named_table(
    named_table: stalg.ReadRel.NamedTable,
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


def _get_child_tables_and_field_offsets(
    child: ir.TableExpr,
) -> tuple[Sequence[ops.TableNode], list[int]]:
    child_op = child.op()
    if isinstance(child_op, ops.Join):
        return [child_op.left, child_op.right], [0, len(child_op.left.op().schema)]
    return [child], [0]


@decompile.register
def _decompile_filter_rel(
    filter_rel: stalg.FilterRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(filter_rel.input, decompiler, names)
    children, field_offsets = _get_child_tables_and_field_offsets(child)
    predicate = decompile(filter_rel.condition, children, field_offsets, decompiler)
    return child.filter(predicate)


@decompile.register
def _decompile_fetch_rel(
    fetch_rel: stalg.FetchRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(fetch_rel.input, decompiler, names)
    return child.limit(fetch_rel.count, offset=fetch_rel.offset)


_JOIN_METHOD_TABLE = {
    stalg.JoinRel.JoinType.JOIN_TYPE_INNER: "inner",
    stalg.JoinRel.JoinType.JOIN_TYPE_OUTER: "outer",
    stalg.JoinRel.JoinType.JOIN_TYPE_LEFT: "left",
    stalg.JoinRel.JoinType.JOIN_TYPE_RIGHT: "right",
    stalg.JoinRel.JoinType.JOIN_TYPE_SEMI: "semi",
    stalg.JoinRel.JoinType.JOIN_TYPE_ANTI: "anti",
}


@decompile.register
def _decompile_join_rel(
    join_rel: stalg.JoinRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    left_child = decompile(join_rel.left, decompiler, names)
    right_child = decompile(join_rel.right, decompiler, names)
    join_method_name = _JOIN_METHOD_TABLE[join_rel.type]
    predicates = decompile(
        join_rel.expression,
        children=[left_child, right_child],
        field_offsets=[0, len(left_child.schema())],
        decompiler=decompiler,
    )
    join_method = getattr(left_child, f"{join_method_name}_join")
    # TODO: implement post_join_filter
    return join_method(right_child, predicates=predicates)


@decompile.register
def _decompile_sort_rel(
    sort_rel: stalg.SortRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(sort_rel.input, decompiler, names)
    children, field_offsets = _get_child_tables_and_field_offsets(child)
    sorts = [
        decompile(sort, children, field_offsets, decompiler) for sort in sort_rel.sorts
    ]
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
    >>> dtype = dt.parse(typestr)
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
    expr: stalg.Expression | stalg.AggregateFunction,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.ValueExpr:
    expr_name = names.popleft()
    ibis_expr = decompile(expr, children, field_offsets, decompiler).name(expr_name)

    # remove child names since those are encoded in the data type
    _remove_names_below(names, ibis_expr.type())

    return ibis_expr


@decompile.register
def _decompile_project_rel(
    project_rel: stalg.ProjectRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    child = decompile(project_rel.input, decompiler, names)
    children, field_offsets = _get_child_tables_and_field_offsets(child)
    exprs = [
        _decompile_with_name(expr, children, field_offsets, decompiler, names)
        for expr in project_rel.expressions
    ]

    return child.projection(exprs)


@decompile.register
def _decompile_aggregate_rel(
    aggregate_rel: stalg.AggregateRel,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    # TODO: aggregate_rel.phase is ignored, do we need to preserve it?
    child = decompile(aggregate_rel.input, decompiler, names)
    children, field_offsets = _get_child_tables_and_field_offsets(child)

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
            _decompile_with_name(
                grouping_expression,
                children,
                field_offsets,
                decompiler,
                names,
            )
            for grouping_expression in grouping_expressions
        )

    metrics = [
        _decompile_with_name(
            agg_rel_measure.measure,
            children,
            field_offsets,
            decompiler,
            names,
        )
        for agg_rel_measure in aggregate_rel.measures
    ]

    return child.aggregate(by=by, metrics=metrics)


@decompile.register
def _decompile_expression_aggregate_function(
    aggregate_function: stalg.AggregateFunction,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    extension = decompiler.function_extensions[aggregate_function.function_reference]
    function_name = extension.name
    op_type = SUBSTRAIT_IBIS_OP_MAPPING[function_name]
    args = [
        decompile(arg, children, field_offsets, decompiler)
        for arg in aggregate_function.arguments
    ]

    # XXX: handle table.count(); what an annoying hack
    if not args and issubclass(op_type, (ops.Count, ops.CountStar)):
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
    left: stalg.Rel,
    right: stalg.Rel,
    *,
    op: stalg.SetRel.SetOp.V,
    decompiler: SubstraitDecompiler,
    names: Deque[str],
) -> ir.TableExpr:
    left_expr = decompile(left, decompiler, names)
    right_expr = decompile(right, decompiler, names)
    name = stalg.SetRel.SetOp.Name(op)
    method = getattr(SetOpDecompiler, f"decompile_{name}", None)
    if method is None:
        raise NotImplementedError(f"set operation not yet implemented: `{name}`")
    return method(left_expr, right_expr)


@decompile.register
def _decompile_set_op_rel(
    set_rel: stalg.SetRel,
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


@functools.singledispatch
def _get_field(
    child: ir.TableExpr | ir.StructValue,
    relative_offset: int,
) -> ir.ValueExpr:
    raise NotImplementedError(f"accessing field of type {type(child)} is not supported")


@_get_field.register(ops.Node)
def _get_field_ops_node(child: ops.Node, relative_offset: int) -> ir.ValueExpr:
    return _get_field(child.to_expr(), relative_offset)


@_get_field.register(ir.TableExpr)
def _get_field_table_expr(child: ir.TableExpr, relative_offset: int) -> ir.ValueExpr:
    return child[relative_offset]


@_get_field.register(ir.StructValue)
def _get_field_struct(child: ir.TableExpr, relative_offset: int) -> ir.ValueExpr:
    field_type = child.type()
    return child[field_type.names[relative_offset]]


class ExpressionDecompiler:
    @staticmethod
    def decompile_literal(
        literal: stalg.Expression.Literal,
        _children: Sequence[ir.TableExpr],
        _offsets: Sequence[int],
        _decompiler: SubstraitDecompiler,
    ) -> ir.ScalarExpr:
        value, dtype = decompile(literal)
        return ibis.literal(value, type=dtype)

    @staticmethod
    def _decompile_struct_field(
        struct_field: stalg.Expression.ReferenceSegment.StructField,
        field_offsets: Sequence[int],
        children: Sequence[ir.TableExpr | ir.StructValue],
    ) -> ir.ValueExpr:
        absolute_offset = struct_field.field

        # get the index of the child relation from a sequence of field_offsets
        child_index = bisect.bisect_right(field_offsets, absolute_offset) - 1
        child = children[child_index]

        # return the field index of the child
        relative_offset = absolute_offset - field_offsets[child_index]

        return _get_field(child, relative_offset)

    @staticmethod
    def decompile_selection(
        ref: stalg.Expression.FieldReference,
        children: Sequence[ir.TableExpr],
        field_offsets: Sequence[int],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        ref_type, ref_variant = which_one_of(ref, "reference_type")
        if ref_type != "direct_reference":
            raise NotImplementedError(
                f"decompilation of `{ref_type}` references are not yet implemented"
            )

        assert isinstance(ref_variant, stalg.Expression.ReferenceSegment)

        _, struct_field = which_one_of(
            ref_variant,
            "reference_type",
        )
        assert isinstance(
            struct_field,
            stalg.Expression.ReferenceSegment.StructField,
        )

        result = ExpressionDecompiler._decompile_struct_field(
            struct_field,
            field_offsets,
            children,
        )

        while struct_field.HasField("child"):
            struct_field = struct_field.child.struct_field
            result = ExpressionDecompiler._decompile_struct_field(
                struct_field,
                field_offsets,
                # the new child is always the previous result
                children=[result],
            )
        return result

    @staticmethod
    def decompile_scalar_function(
        scalar_func: stalg.Expression.ScalarFunction,
        children: Sequence[ir.TableExpr],
        field_offsets: Sequence[int],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return decompile(scalar_func, children, field_offsets, decompiler)

    @staticmethod
    def decompile_if_then(
        if_then: stalg.Expression.IfThen,
        children: Sequence[ir.TableExpr],
        offsets: Sequence[int],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return decompile(if_then, children, offsets, decompiler)

    @staticmethod
    def decompile_singular_or_list(
        singular_or_list: stalg.Expression.SingularOrList,
        children: Sequence[ir.TableExpr],
        offsets: Sequence[int],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return decompile(singular_or_list, children, offsets, decompiler)

    @staticmethod
    def decompile_cast(
        cast: stalg.Expression.Cast,
        children: Sequence[ir.TableExpr],
        offsets: Sequence[int],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return decompile(cast, children, offsets, decompiler)

    @staticmethod
    def decompile_enum(
        enum: stalg.Expression.Enum,
        children: Sequence[ir.TableExpr],
        offsets: Sequence[int],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return decompile(enum)


@decompile.register
def _decompile_function_argument(
    msg: stalg.FunctionArgument,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    arg_type_name, arg = which_one_of(msg, "arg_type")
    method = getattr(FunctionArgumentDecompiler, f"decompile_{arg_type_name}", None)
    if method is None:
        raise NotImplementedError(
            f"decompilation of {arg_type_name!r} function argument not implemented"
        )
    return method(arg, children, field_offsets, decompiler)


class FunctionArgumentDecompiler:
    @staticmethod
    def decompile_value(
        msg: stalg.Expression,
        children: Sequence[ir.TableExpr],
        field_offsets: Sequence[int],
        decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return decompile(msg, children, field_offsets, decompiler)

    @staticmethod
    def decompile_enum(
        msg: str,
        _children: Sequence[ir.TableExpr],
        _field_offsets: Sequence[int],
        _decompiler: SubstraitDecompiler,
    ) -> ir.ValueExpr:
        return msg


@decompile.register
def _decompile_expression(
    msg: stalg.Expression,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    rex_type_name, rex = which_one_of(msg, "rex_type")
    method = getattr(ExpressionDecompiler, f"decompile_{rex_type_name}", None)
    if method is None:
        raise NotImplementedError(
            f"decompilation of {rex_type_name!r} expression variant not implemented"
        )
    return method(rex, children, field_offsets, decompiler)


@decompile.register
def _decompile_expression_scalar_function(
    msg: stalg.Expression.ScalarFunction,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    extension = decompiler.function_extensions[msg.function_reference]
    function_name = extension.name
    op_type = SUBSTRAIT_IBIS_OP_MAPPING[function_name]
    args = [
        decompile(arg, children, field_offsets, decompiler) for arg in msg.arguments
    ]
    expr = op_type(*args).to_expr()
    output_type = _decompile_type(msg.output_type)
    if expr.type() != output_type:
        return expr.cast(output_type)
    return expr


@decompile.register
def _decompile_expression_sort_field(
    msg: stalg.SortField,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    expr = decompile(msg.expr, children, field_offsets, decompiler)
    sort_field_func = _decompile_sort_field_type(msg.direction)
    return sort_field_func(expr)


def _decompile_sort_field_type(
    sort_type: stalg.SortField.SortDirection.V,
) -> Callable[[T], Any]:
    if sort_type in {
        stalg.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_FIRST,
        stalg.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_LAST,
    }:
        return toolz.identity
    elif sort_type in {
        stalg.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_FIRST,
        stalg.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_LAST,
    }:
        return ibis.desc
    else:
        raise NotImplementedError(f"unknown sort type when decompiling: `{sort_type}`")


@decompile.register
def _decompile_expression_if_then(
    msg: stalg.Expression.IfThen,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    ifs, thens = zip(
        *[
            (
                decompile(getattr(_if, "if"), children, field_offsets, decompiler),
                decompile(_if.then, children, field_offsets, decompiler),
            )
            for _if in msg.ifs
        ]
    )
    base_op = ifs[0].op()

    return decompile(base_op, msg, children, field_offsets, decompiler, ifs, thens)


@decompile.register
def _decompile_if_then_comparison(
    base_op: ops.Comparison,
    msg: stalg.Expression.IfThen,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
    ifs: Sequence[ir.ValueExpr],
    thens: Sequence[ir.ValueExpr],
) -> ir.ValueExpr:
    if len(ifs) > 1:
        assert all(
            _if.op().left.op().name == base_op.left.op().name for _if in ifs[1:]
        ), "SimpleCase should compare against same column"
    base_case = base_op.left.op().to_expr().case()
    for case, result in zip((_if.op().right for _if in ifs), thens):
        base_case = base_case.when(case, result)
    return base_case.else_(
        decompile(getattr(msg, "else"), children, field_offsets, decompiler)
    ).end()


@decompile.register
def _decompile_if_then_stringlike(
    base_op: ops.StringSQLLike,
    msg: stalg.Expression.IfThen,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
    ifs: Sequence[ir.ValueExpr],
    thens: Sequence[ir.ValueExpr],
) -> ir.ValueExpr:
    assert len(thens) == 1, "only one result in a stringlike"

    return (
        base_op.arg.op()
        .to_expr()
        .like(base_op.pattern)
        .ifelse(
            thens[0],
            decompile(getattr(msg, "else"), children, field_offsets, decompiler),
        )
    )


@decompile.register
def _decompile_expression_singular_or_list(
    msg: stalg.Expression.SingularOrList,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    column = decompile(msg.value, children, field_offsets, decompiler)
    return column.isin(
        [decompile(value, children, field_offsets, decompiler) for value in msg.options]
    )


@decompile.register
def _decompile_expression_cast(
    msg: stalg.Expression.Cast,
    children: Sequence[ir.TableExpr],
    field_offsets: Sequence[int],
    decompiler: SubstraitDecompiler,
) -> ir.ValueExpr:
    column = decompile(msg.input, children, field_offsets, decompiler)
    return column.cast(_decompile_type(msg.type))


@decompile.register
def _decompile_expression_enum(
    msg: stalg.Expression.Enum,
) -> str:
    return msg.specified


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
        value: stalg.Expression.Literal.List,
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
    def decompile_fixed_char(value: str) -> tuple[str, dt.String]:
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
        value: stalg.Expression.Literal.Map,
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


@decompile.register(stalg.Expression.Literal)
def _decompile_literal(msg: stalg.Expression.Literal) -> tuple[T, dt.DataType]:
    literal_type_name, literal = which_one_of(msg, "literal_type")
    method = getattr(LiteralDecompiler, f"decompile_{literal_type_name}", None)
    if method is None:
        raise NotImplementedError(
            f"decompilation of `{literal_type_name}` literals not yet implemented"
        )
    return method(literal)
