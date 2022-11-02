"""Turn ibis things into substrait things.

The primary API exposed here is the :func:`translate` function.
"""

from __future__ import annotations

import collections
import collections.abc
import datetime
import decimal
import functools
import itertools
import math
import operator
import uuid
from typing import Any, Mapping, MutableMapping, Sequence, TypeVar

import ibis
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.schema as sch
import ibis.expr.types as ir
import toolz
from ibis import util
from ibis.util import to_op_dag

from ..proto.substrait.ibis import algebra_pb2 as stalg
from ..proto.substrait.ibis import type_pb2 as stt
from .core import SubstraitCompiler, _get_fields

T = TypeVar("T")


def _nullability(dtype: dt.DataType) -> stt.Type.Nullability.V:
    return (
        stt.Type.Nullability.NULLABILITY_NULLABLE
        if dtype.nullable
        else stt.Type.Nullability.NULLABILITY_REQUIRED
    )


@functools.singledispatch
def translate(*args: Any, **kwargs: Any) -> Any:
    raise NotImplementedError(*args)


@translate.register
def _boolean(dtype: dt.Boolean) -> stt.Type:
    return stt.Type(bool=stt.Type.Boolean(nullability=_nullability(dtype)))


@translate.register
def _i8(dtype: dt.Int8) -> stt.Type:
    return stt.Type(i8=stt.Type.I8(nullability=_nullability(dtype)))


@translate.register
def _i16(dtype: dt.Int16) -> stt.Type:
    return stt.Type(i16=stt.Type.I16(nullability=_nullability(dtype)))


@translate.register
def _i32(dtype: dt.Int32) -> stt.Type:
    return stt.Type(i32=stt.Type.I32(nullability=_nullability(dtype)))


@translate.register
def _i64(dtype: dt.Int64) -> stt.Type:
    return stt.Type(i64=stt.Type.I64(nullability=_nullability(dtype)))


@translate.register
def _float32(dtype: dt.Float32) -> stt.Type:
    return stt.Type(fp32=stt.Type.FP32(nullability=_nullability(dtype)))


@translate.register
def _float64(dtype: dt.Float64) -> stt.Type:
    return stt.Type(fp64=stt.Type.FP64(nullability=_nullability(dtype)))


@translate.register
def _string(dtype: dt.String) -> stt.Type:
    return stt.Type(string=stt.Type.String(nullability=_nullability(dtype)))


@translate.register
def _binary(dtype: dt.Binary) -> stt.Type:
    return stt.Type(binary=stt.Type.Binary(nullability=_nullability(dtype)))


@translate.register
def _date(dtype: dt.Date) -> stt.Type:
    return stt.Type(date=stt.Type.Date(nullability=_nullability(dtype)))


@translate.register
def _time(dtype: dt.Time) -> stt.Type:
    return stt.Type(time=stt.Type.Time(nullability=_nullability(dtype)))


@translate.register
def _decimal(dtype: dt.Decimal) -> stt.Type:
    return stt.Type(
        decimal=stt.Type.Decimal(
            scale=dtype.scale,
            precision=dtype.precision,
            nullability=_nullability(dtype),
        )
    )


@translate.register
def _timestamp(dtype: dt.Timestamp) -> stt.Type:
    nullability = _nullability(dtype)
    if dtype.timezone is not None:
        return stt.Type(timestamp_tz=stt.Type.TimestampTZ(nullability=nullability))
    return stt.Type(timestamp=stt.Type.Timestamp(nullability=nullability))


@translate.register
def _interval(dtype: dt.Interval) -> stt.Type:
    unit = dtype.unit
    nullability = _nullability(dtype)

    if unit == "Y":
        return stt.Type(interval_year=stt.Type.IntervalYear(nullability=nullability))
    elif unit == "M":
        return stt.Type(interval_year=stt.Type.IntervalYear(nullability=nullability))
    elif unit == "D":
        return stt.Type(interval_day=stt.Type.IntervalDay(nullability=nullability))
    elif unit == "s":
        return stt.Type(interval_day=stt.Type.IntervalDay(nullability=nullability))

    raise ValueError(f"unsupported substrait unit: {unit!r}")


@translate.register
def _array(dtype: dt.Array) -> stt.Type:
    return stt.Type(
        list=stt.Type.List(
            type=translate(dtype.value_type),
            nullability=_nullability(dtype),
        )
    )


@translate.register
def _map(dtype: dt.Map) -> stt.Type:
    return stt.Type(
        map=stt.Type.Map(
            key=translate(dtype.key_type),
            value=translate(dtype.value_type),
            nullability=_nullability(dtype),
        )
    )


def _struct(
    struct: dt.Struct,
    *,
    nullability: stt.Type.Nullability.V,
) -> stt.Type.Struct:
    return stt.Type.Struct(
        types=list(map(translate, struct.types)),
        nullability=nullability,
    )


@translate.register
def _struct_type(dtype: dt.Struct) -> stt.Type:
    return stt.Type(struct=_struct(dtype, nullability=_nullability(dtype)))


@translate.register
def _schema(schema: sch.Schema) -> stt.NamedStruct:
    fields = list(zip(reversed(schema.names), reversed(schema.types)))
    names = []

    while fields:
        name, typ = fields.pop()

        # arrays and and maps aren't named so we don't store the None
        # placeholder used to ensure that we traverse down their key/value
        # types
        if name is not None:
            names.append(name)

        fields.extend(_get_fields(typ))

    return stt.NamedStruct(
        names=names,
        struct=stt.Type.Struct(
            types=list(map(translate, schema.types)),
            nullability=stt.Type.Nullability.NULLABILITY_REQUIRED,
        ),
    )


@translate.register(ir.Expr)
def _expr(
    expr: ir.Expr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return translate(expr.op(), expr, compiler, **kwargs)


@translate.register(ops.Literal)
def _literal(
    op: ops.Literal,
    expr: ir.ScalarExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    dtype = expr.type()
    value = op.value
    if value is None:
        return stalg.Expression(
            literal=stalg.Expression.Literal(null=translate(dtype, **kwargs))
        )
    return stalg.Expression(literal=translate_literal(dtype, op.value))


@functools.singledispatch
def translate_literal(
    dtype: dt.DataType,
    op: object,
) -> stalg.Expression.Literal:
    raise NotImplementedError(
        f"{dtype.__class__.__name__} literals are not yet implemented"
    )


@translate.register
def _null_literal(_: dt.Null, **kwargs: Any) -> stalg.Expression.Literal:
    raise NotImplementedError("untyped null literals are not supported")


@translate_literal.register
def _literal_boolean(
    dtype: dt.Boolean,
    value: bool,
) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(boolean=value)


@translate_literal.register
def _literal_int8(_: dt.Int8, value: int) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(i8=value)


@translate_literal.register
def _literal_int16(_: dt.Int16, value: int) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(i16=value)


@translate_literal.register
def _literal_int32(_: dt.Int32, value: int) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(i32=value)


@translate_literal.register
def _literal_int64(d_: dt.Int64, value: int) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(i64=value)


@translate_literal.register
def _literal_float32(_: dt.Float32, value: float) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(fp32=value)


@translate_literal.register
def _literal_float64(_: dt.Float64, value: float) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(fp64=value)


@translate_literal.register
def _literal_decimal(
    dtype: dt.Decimal, value: decimal.Decimal
) -> stalg.Expression.Literal:
    raise NotImplementedError


@translate_literal.register
def _literal_string(_: dt.String, value: str) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(string=value)


@translate_literal.register
def _literal_binary(_: dt.Binary, value: bytes) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(binary=value)


@translate_literal.register
def _literal_timestamp(
    dtype: dt.Timestamp,
    value: datetime.datetime,
) -> stalg.Expression.Literal:
    micros_since_epoch = int(value.timestamp() * 1e6)
    if dtype.timezone is not None:
        return stalg.Expression.Literal(timestamp_tz=micros_since_epoch)
    return stalg.Expression.Literal(timestamp=micros_since_epoch)


@translate_literal.register
def _literal_struct(
    dtype: dt.Struct,
    mapping: collections.OrderedDict,
) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(
        struct=stalg.Expression.Literal.Struct(
            fields=[
                translate_literal(field_type, val)
                for val, field_type in zip(mapping.values(), dtype.types)
            ]
        )
    )


@translate_literal.register
def _literal_map(
    dtype: dt.Map,
    mapping: collections.abc.MutableMapping,
) -> stalg.Expression.Literal:
    if not mapping:
        return stalg.Expression.Literal(empty_map=translate(dtype).map)
    return stalg.Expression.Literal(
        map=stalg.Expression.Literal.Map(
            key_values=[
                stalg.Expression.Literal.Map.KeyValue(
                    key=translate_literal(dtype.key_type, key),
                    value=translate_literal(dtype.value_type, value),
                )
                for key, value in mapping.items()
            ],
        )
    )


@translate_literal.register
def _literal_array(
    dtype: dt.Array,
    sequence: Sequence[T],
) -> stalg.Expression.Literal:
    if not sequence:
        return stalg.Expression.Literal(empty_list=translate(dtype).list)
    return stalg.Expression.Literal(
        list=stalg.Expression.Literal.List(
            values=[translate_literal(dtype.value_type, value) for value in sequence],
        )
    )


@translate_literal.register(dt.UUID)
def _literal_uuid(dtype: dt.UUID, value: str | uuid.UUID) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(uuid=uuid.UUID(hex=str(value)).bytes)


_MINUTES_PER_HOUR = _SECONDS_PER_MINUTE = 60
_MICROSECONDS_PER_SECOND = 1_000_000


def _time_to_micros(value: datetime.time) -> int:
    """Convert a Python ``datetime.time`` object to microseconds since day-start."""
    return (
        value.hour * _MINUTES_PER_HOUR * _SECONDS_PER_MINUTE * _MICROSECONDS_PER_SECOND
        + value.minute * _SECONDS_PER_MINUTE * _MICROSECONDS_PER_SECOND
        + value.second * _MICROSECONDS_PER_SECOND
        + value.microsecond
    )


@translate_literal.register
def _literal_time(time: dt.Time, value: datetime.time) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(time=_time_to_micros(value))


def _date_to_days(value: datetime.date) -> int:
    delta = value - datetime.datetime.utcfromtimestamp(0).date()
    return delta.days


@translate_literal.register
def _literal_date(date: dt.Date, value: datetime.date) -> stalg.Expression.Literal:
    return stalg.Expression.Literal(date=_date_to_days(value))


@functools.singledispatch
def translate_preceding(value: int | None) -> stalg.Expression.WindowFunction.Bound:
    raise NotImplementedError()


@translate_preceding.register
def _preceding_none(_: None) -> stalg.Expression.WindowFunction.Bound:
    return stalg.Expression.WindowFunction.Bound(
        unbounded=stalg.Expression.WindowFunction.Bound.Unbounded()
    )


@translate_preceding.register
def _preceding_int(offset: int) -> stalg.Expression.WindowFunction.Bound:
    return stalg.Expression.WindowFunction.Bound(
        preceding=stalg.Expression.WindowFunction.Bound.Preceding(offset=offset)
    )


@functools.singledispatch
def translate_following(value: int | None) -> stalg.Expression.WindowFunction.Bound:
    raise NotImplementedError()


@translate_following.register
def _following_none(_: None) -> stalg.Expression.WindowFunction.Bound:
    return translate_preceding(_)


@translate_following.register
def _following_int(offset: int) -> stalg.Expression.WindowFunction.Bound:
    return stalg.Expression.WindowFunction.Bound(
        following=stalg.Expression.WindowFunction.Bound.Following(offset=offset)
    )


def _translate_window_bounds(
    precedes: tuple[int, int] | int | None,
    follows: tuple[int, int] | int | None,
) -> tuple[
    stalg.Expression.WindowFunction.Bound,
    stalg.Expression.WindowFunction.Bound,
]:
    # all preceding or all following or one or the other
    preceding = util.promote_list(precedes)
    following = util.promote_list(follows)

    if len(preceding) == 2:
        if following:
            raise ValueError(
                "`following` not allowed when window bounds are both preceding"
            )

        lower, upper = preceding
        return translate_preceding(lower), translate_preceding(upper)

    if len(preceding) != 1:
        raise ValueError(f"preceding must be length 1 or 2 got: {len(preceding)}")

    if len(following) == 2:
        if preceding:
            raise ValueError(
                "`preceding` not allowed when window bounds are both following"
            )

        lower, upper = following
        return translate_following(lower), translate_following(upper)
    elif len(following) != 1:
        raise ValueError(f"following must be length 1 or 2 got: {len(following)}")

    return translate_preceding(*preceding), translate_following(*following)


@translate.register(ops.Alias)
def alias_op(
    op: ops.Alias,
    expr: ir.ValueExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # For an alias, dispatch on the underlying argument
    return translate(op.arg.op(), op.arg, compiler, **kwargs)


@translate.register(ops.ValueOp)
def value_op(
    op: ops.ValueOp,
    expr: ir.ValueExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    error_args = []
    # TODO(gforsyth): remove this brittle workaround after extension parsing is ready
    # TODO(gforsyth): sending in `ERROR` for floating point ops doesn't match
    # the substrait spec but is what pyarrow currently expects.
    if (
        isinstance(op, ops.BinaryOp)
        and not isinstance(op, ops.Comparison)
        and isinstance(op.left.type(), (dt.Integer, dt.Floating))
        and isinstance(op.right.type(), (dt.Integer, dt.Floating))
    ):
        error_args.append(
            stalg.FunctionArgument(enum=stalg.FunctionArgument.Enum(specified="ERROR"))
        )

    # given the details of `op` -> function id
    return stalg.Expression(
        scalar_function=stalg.Expression.ScalarFunction(
            function_reference=compiler.function_id(expr),
            output_type=translate(expr.type()),
            arguments=error_args
            + [
                stalg.FunctionArgument(value=translate(arg, compiler, **kwargs))
                for arg in op.args
                if isinstance(arg, ir.Expr)
            ],
        )
    )


@translate.register(ops.WindowOp)
def window_op(
    op: ops.WindowOp,
    expr: ir.ValueExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    lower_bound, upper_bound = _translate_window_bounds(
        op.window.preceding, op.window.following
    )
    return stalg.Expression(
        window_function=stalg.Expression.WindowFunction(
            function_reference=compiler.function_id(op.expr),
            partitions=[
                translate(gb, compiler, **kwargs) for gb in op.window._group_by
            ],
            sorts=[translate(ob, compiler, **kwargs) for ob in op.window._order_by],
            output_type=translate(expr.type()),
            phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
            arguments=[
                stalg.FunctionArgument(value=translate(arg, compiler, **kwargs))
                for arg in op.expr.op().args
                if isinstance(arg, ir.Expr)
            ],
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )
    )


@translate.register(ops.Reduction)
def _reduction(
    op: ops.Reduction,
    expr: ir.ScalarExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.AggregateFunction:
    return stalg.AggregateFunction(
        function_reference=compiler.function_id(expr),
        arguments=[stalg.FunctionArgument(value=translate(op.arg, compiler, **kwargs))],
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(expr.type()),
    )


@translate.register(ops.Count)
def _count(
    op: ops.Count,
    expr: ir.ScalarExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.AggregateFunction:
    translated_args = []
    arg = op.arg
    if not isinstance(arg, ir.TableExpr):
        translated_args.append(
            stalg.FunctionArgument(value=translate(arg, compiler, **kwargs))
        )
    return stalg.AggregateFunction(
        function_reference=compiler.function_id(expr),
        arguments=translated_args,
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(expr.type()),
    )


@translate.register(ops.SortKey)
def sort_key(
    op: ops.SortKey,
    expr: ir.SortExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.SortField:
    ordering = "ASC" if op.ascending else "DESC"
    return stalg.SortField(
        expr=translate(op.expr, compiler, **kwargs),
        direction=getattr(
            stalg.SortField.SortDirection,
            f"SORT_DIRECTION_{ordering}_NULLS_FIRST",
        ),
    )


@translate.register(ops.TableColumn)
def table_column(
    op: ops.TableColumn,
    expr: ir.ColumnExpr,
    _: SubstraitCompiler,
    *,
    child_rel_field_offsets: MutableMapping[ops.TableNode, int] | None = None,
    **kwargs: Any,
) -> stalg.Expression:
    schema = op.table.schema()
    relative_offset = schema._name_locs[op.name]
    base_offset = (child_rel_field_offsets or {}).get(op.table.op(), 0)
    absolute_offset = base_offset + relative_offset
    return stalg.Expression(
        selection=stalg.Expression.FieldReference(
            root_reference=stalg.Expression.FieldReference.RootReference(),
            direct_reference=stalg.Expression.ReferenceSegment(
                struct_field=stalg.Expression.ReferenceSegment.StructField(
                    field=absolute_offset,
                ),
            ),
        )
    )


@translate.register(ops.StructField)
def struct_field(
    op: ops.StructField,
    _: ir.ColumnExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    child = translate(op.arg, compiler=compiler, **kwargs)
    field_name = op.field
    # TODO: store names/types inverse mapping on datatypes.Struct for O(1)
    # access to field index
    field_index = op.arg.type().names.index(field_name)

    struct_field = child.selection.direct_reference.struct_field

    # keep digging until we bottom out on the deepest child reference which
    # becomes the parent for the returned reference
    while struct_field.HasField("child"):
        struct_field = struct_field.child.struct_field

    struct_field.child.MergeFrom(
        stalg.Expression.ReferenceSegment(
            struct_field=stalg.Expression.ReferenceSegment.StructField(
                field=field_index
            )
        )
    )

    return child


@translate.register(ops.UnboundTable)
def unbound_table(
    op: ops.UnboundTable, expr: ir.TableExpr, _: SubstraitCompiler, **kwargs: Any
) -> stalg.Rel:
    return stalg.Rel(
        read=stalg.ReadRel(
            # TODO: filter,
            # TODO: projection,
            common=stalg.RelCommon(direct=stalg.RelCommon.Direct()),
            base_schema=translate(op.schema),
            named_table=stalg.ReadRel.NamedTable(names=[op.name]),
        )
    )


def _get_child_relation_field_offsets(table: ir.TableExpr) -> dict[ops.TableNode, int]:
    """Return the offset of each of table's fields.

    This function calculates the starting index of a relations fields, as if
    all relations were part of a single flat schema.

    Examples
    --------
    >>> import ibis
    >>> t1 = ibis.table(
    ...     [("a", "int64"), ("b", "string"), ("c", "array<int64>")],
    ...     name="t1",
    ... )
    >>> t2 = ibis.table([("d", "string"), ("e", "map<string, float64>")], name="t2")
    >>> expr = t1.join(t2, t1.b == t2.d)
    >>> mapping = _get_child_relation_field_offsets(expr)
    >>> mapping[t1.op()]  # the first relation is always zero
    0
    >>> mapping[t2.op()]  # first relation has 3 fields, so the second starts at 3
    3
    """
    table_op = table.op()
    if isinstance(table_op, ops.Join):
        # Descend into the left and right tables to grab offsets from nested joins
        left_keys = _get_child_relation_field_offsets(table_op.left)
        right_keys = _get_child_relation_field_offsets(table_op.right)
        root_tables = [table_op.left.op(), table_op.right.op()]
        accum = [0, len(root_tables[0].schema)]
        return toolz.merge(left_keys, right_keys, dict(zip(root_tables, accum)))
    return {}


@translate.register(ops.Selection)
def selection(
    op: ops.Selection,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    child_rel_field_offsets: Mapping[ops.TableNode, int] | None = None,
    **kwargs: Any,
) -> stalg.Rel:
    assert (
        not child_rel_field_offsets
    ), "non-empty child_rel_field_offsets passed in to selection translation rule"
    child_rel_field_offsets = _get_child_relation_field_offsets(op.table)
    # source
    relation = translate(
        op.table,
        compiler,
        child_rel_field_offsets=child_rel_field_offsets,
        **kwargs,
    )
    # filter
    if op.predicates:
        relation = stalg.Rel(
            filter=stalg.FilterRel(
                input=relation,
                condition=translate(
                    functools.reduce(operator.and_, op.predicates),
                    compiler,
                    child_rel_field_offsets=child_rel_field_offsets,
                    **kwargs,
                ),
            )
        )

    # projection / emit
    selections = [
        col
        for sel in op.selections
        for col in (
            sel.get_columns(sel.columns) if isinstance(sel, ir.TableExpr) else [sel]
        )
    ]

    # TODO: there has to be a better way to get a list of source tables
    # underlying an expression
    # TODO: settle on a better source table definition than "PhysicalTable with
    # a schema"
    source_tables = {
        t
        for t in to_op_dag(op.to_expr()).keys()
        if isinstance(t, ops.PhysicalTable) and hasattr(t, "schema")
    }
    mapping_counter = itertools.count(sum(len(t.schema) for t in source_tables))
    if selections:

        if relation.project.common.ListFields():
            # if there is already an `emit` in RelCommon then we're stacking
            # projections and we need to update the output_mapping to refer to
            # the number of fields present in the most recent emit
            mapping_counter = itertools.count(
                len(relation.project.common.emit.output_mapping)
            )

        relation = stalg.Rel(
            project=stalg.ProjectRel(
                input=relation,
                common=stalg.RelCommon(
                    emit=stalg.RelCommon.Emit(
                        output_mapping=[next(mapping_counter) for _ in selections]
                    )
                ),
                expressions=[
                    translate(
                        selection,
                        compiler,
                        child_rel_field_offsets=child_rel_field_offsets,
                        **kwargs,
                    )
                    for selection in selections
                ],
            )
        )

    # order by
    if op.sort_keys:
        relation = stalg.Rel(
            sort=stalg.SortRel(
                input=relation,
                sorts=[
                    translate(
                        key,
                        compiler,
                        child_rel_field_offsets=child_rel_field_offsets,
                        **kwargs,
                    )
                    for key in op.sort_keys
                ],
            )
        )

    return relation


@functools.singledispatch
def _translate_join_type(op: ops.Join) -> stalg.JoinRel.JoinType.V:
    raise NotImplementedError(f"join type `{type(op).__name__}` not implemented")


@_translate_join_type.register(ops.InnerJoin)
def _translate_inner_join(_: ops.InnerJoin) -> stalg.JoinRel.JoinType.V:
    return stalg.JoinRel.JoinType.JOIN_TYPE_INNER


@_translate_join_type.register(ops.OuterJoin)
def _translate_outer_join(_: ops.OuterJoin) -> stalg.JoinRel.JoinType.V:
    return stalg.JoinRel.JoinType.JOIN_TYPE_OUTER


@_translate_join_type.register(ops.LeftJoin)
def _translate_left_join(_: ops.LeftJoin) -> stalg.JoinRel.JoinType.V:
    return stalg.JoinRel.JoinType.JOIN_TYPE_LEFT


@_translate_join_type.register(ops.RightJoin)
def _translate_right_join(_: ops.RightJoin) -> stalg.JoinRel.JoinType.V:
    return stalg.JoinRel.JoinType.JOIN_TYPE_RIGHT


@_translate_join_type.register(ops.LeftSemiJoin)
def _translate_semi_join(_: ops.LeftSemiJoin) -> stalg.JoinRel.JoinType.V:
    return stalg.JoinRel.JoinType.JOIN_TYPE_SEMI


@_translate_join_type.register(ops.LeftAntiJoin)
def _translate_anti_join(_: ops.LeftAntiJoin) -> stalg.JoinRel.JoinType.V:
    return stalg.JoinRel.JoinType.JOIN_TYPE_ANTI


@translate.register(ops.Join)
def join(
    op: ops.Join,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    child_rel_field_offsets = kwargs.pop("child_rel_field_offsets", None)
    child_rel_field_offsets = (
        child_rel_field_offsets or _get_child_relation_field_offsets(expr)
    )
    return stalg.Rel(
        join=stalg.JoinRel(
            left=translate(op.left, compiler, **kwargs),
            right=translate(op.right, compiler, **kwargs),
            expression=translate(
                functools.reduce(operator.and_, op.predicates),
                compiler,
                child_rel_field_offsets=child_rel_field_offsets,
                **kwargs,
            ),
            type=_translate_join_type(op),
        )
    )


@translate.register(ops.Limit)
def limit(
    op: ops.Limit,
    expr: ir.Expr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    return stalg.Rel(
        fetch=stalg.FetchRel(
            input=translate(op.table, compiler, **kwargs),
            offset=op.offset,
            count=op.n,
        )
    )


@functools.singledispatch
def translate_set_op_type(op: ops.SetOp) -> stalg.SetRel.SetOp.V:
    raise NotImplementedError(
        f"set operation `{type(op).__name__}` not yet implemented"
    )


@translate_set_op_type.register(ops.Union)
def set_op_type_union(op: ops.Union) -> stalg.SetRel.SetOp.V:
    if op.distinct:
        return stalg.SetRel.SetOp.SET_OP_UNION_DISTINCT
    return stalg.SetRel.SetOp.SET_OP_UNION_ALL


@translate_set_op_type.register(ops.Intersection)
def set_op_type_intersection(op: ops.Intersection) -> stalg.SetRel.SetOp.V:
    return stalg.SetRel.SetOp.SET_OP_INTERSECTION_PRIMARY


@translate_set_op_type.register(ops.Difference)
def set_op_type_difference(op: ops.Difference) -> stalg.SetRel.SetOp.V:
    return stalg.SetRel.SetOp.SET_OP_MINUS_PRIMARY


@translate.register(ops.SetOp)
def set_op(
    op: ops.SetOp,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    return stalg.Rel(
        set=stalg.SetRel(
            inputs=[
                translate(op.left, compiler, **kwargs),
                translate(op.right, compiler, **kwargs),
            ],
            op=translate_set_op_type(op),
        )
    )


@translate.register(ops.Aggregation)
def aggregation(
    op: ops.Aggregation,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    if op.having:
        raise NotImplementedError("`having` not yet implemented")

    table = op.table
    predicates = op.predicates
    input = translate(
        table.filter(predicates) if predicates else table,
        compiler,
        **kwargs,
    )

    # TODO: we handle sorts before aggregation here but we shouldn't be
    #
    # sorts should be compiled after after aggregation, because that is
    # semantically where they belong, but due to ibis storing sort keys in the
    # aggregate class we have to sort first, so ibis will use the correct base
    # table when decompiling
    if op.sort_keys:
        sorts = [translate(key, compiler, **kwargs) for key in op.sort_keys]
        input = stalg.Rel(sort=stalg.SortRel(input=input, sorts=sorts))

    aggregate = stalg.AggregateRel(
        input=input,
        groupings=[
            stalg.AggregateRel.Grouping(
                grouping_expressions=[translate(by, compiler, **kwargs)]
            )
            for by in op.by
        ],
        measures=[
            stalg.AggregateRel.Measure(measure=translate(metric, compiler, **kwargs))
            for metric in op.metrics
        ],
    )

    return stalg.Rel(aggregate=aggregate)


@translate.register(ops.SimpleCase)
@translate.register(ops.SearchedCase)
def _simple_searched_case(
    op: ops.SimpleCase | ops.SearchedCase,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # the field names for an `if_then` are `if` and `else` which means we need
    # to pass those args in as a dictionary to not run afoul of SyntaxErrors`
    _ifs = []
    for case, result in zip(op.cases, op.results):
        if_expr = case if not hasattr(op, "base") else op.base == case
        _if = {
            "if": translate(if_expr, compiler, **kwargs),
            "then": translate(result, compiler, **kwargs),
        }
        _ifs.append(stalg.Expression.IfThen.IfClause(**_if))

    _else = {"else": translate(op.default, compiler, **kwargs)}

    return stalg.Expression(if_then=stalg.Expression.IfThen(ifs=_ifs, **_else))


@translate.register(ops.Where)
def _where(
    op: ops.Where,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # the field names for an `if_then` are `if` and `else` which means we need
    # to pass those args in as a dictionary to not run afoul of SyntaxErrors`
    _if = {
        "if": translate(op.bool_expr, compiler, **kwargs),
        "then": translate(op.true_expr, compiler, **kwargs),
    }
    _else = {"else": translate(op.false_null_expr, compiler, **kwargs)}

    _ifs = [stalg.Expression.IfThen.IfClause(**_if)]

    return stalg.Expression(if_then=stalg.Expression.IfThen(ifs=_ifs, **_else))


@translate.register(ops.Contains)
def _contains(
    op: ops.Contains,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return stalg.Expression(
        singular_or_list=stalg.Expression.SingularOrList(
            value=translate(op.value, compiler, **kwargs),
            options=[translate(value, compiler, **kwargs) for value in op.options],
        )
    )


@translate.register(ops.Cast)
def _cast(
    op: ops.Cast,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return stalg.Expression(
        cast=stalg.Expression.Cast(
            type=translate(op.to), input=translate(op.arg, compiler, **kwargs)
        )
    )


@translate.register(ops.ExtractDateField)
def _extractdatefield(
    op: ops.ExtractDateField,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # e.g. "ExtractYear" -> "YEAR"
    span = type(op).__name__[len("Extract") :].upper()
    arguments = (
        stalg.FunctionArgument(value=translate(arg, compiler, **kwargs))
        for arg in op.args
        if isinstance(arg, ir.Expr)
    )

    scalar_func = stalg.Expression.ScalarFunction(
        function_reference=compiler.function_id(expr),
        output_type=translate(expr.type()),
    )
    scalar_func.arguments.add(enum=stalg.FunctionArgument.Enum(specified=span))
    scalar_func.arguments.extend(arguments)
    return stalg.Expression(scalar_function=scalar_func)


@translate.register(ops.Log)
def _log(
    op: ops.Log,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    arg = stalg.FunctionArgument(value=translate(op.arg, compiler, **kwargs))
    base = stalg.FunctionArgument(
        value=translate(
            op.base if op.base is not None else ibis.literal(math.e), compiler, **kwargs
        )
    )

    scalar_func = stalg.Expression.ScalarFunction(
        function_reference=compiler.function_id(expr),
        output_type=translate(expr.type()),
        arguments=[arg, base],
    )
    return stalg.Expression(scalar_function=scalar_func)


@translate.register(ops.FloorDivide)
def _floordivide(
    op: ops.FloorDivide,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    left, right = op.left, op.right
    return translate((left / right).floor(), compiler, **kwargs)
