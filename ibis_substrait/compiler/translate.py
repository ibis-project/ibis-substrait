"""Turn ibis things into substrait things.

The primary API exposed here is the :func:`translate` function.
"""

from __future__ import annotations

import collections
import collections.abc
import datetime
import functools
import operator
import uuid
from typing import Any, MutableMapping, Sequence, TypeVar

import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.schema as sch
import ibis.expr.types as ir
from ibis import util

from ..proto.substrait import expression_pb2 as stexpr
from ..proto.substrait import relations_pb2 as strel
from ..proto.substrait import type_pb2 as stt
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
        decimal=stt.Type.Decimal(scale=dtype.scale, precision=dtype.precision)
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
        struct=stt.Type.Struct(types=list(map(translate, schema.types))),
    )


@translate.register(ir.Expr)
def _expr(
    expr: ir.Expr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stexpr.Expression:
    return translate(expr.op(), expr, compiler, **kwargs)


@translate.register(ops.Literal)
def _literal(
    op: ops.Literal,
    expr: ir.ScalarExpr,
    compiler: SubstraitCompiler,
    **_: Any,
) -> stexpr.Expression:
    dtype = expr.type()
    value = op.value
    if value is None:
        return stexpr.Expression(
            literal=stexpr.Expression.Literal(null=translate(dtype))
        )
    return stexpr.Expression(literal=translate_literal(dtype, op.value))


@functools.singledispatch
def translate_literal(
    dtype: dt.DataType,
    op: object,
) -> stexpr.Expression.Literal:
    raise NotImplementedError(
        f"{dtype.__class__.__name__} literals are not yet implemented"
    )


@translate.register
def _null_literal(_: dt.Null, **kwargs: Any) -> stexpr.Expression.Literal:
    raise NotImplementedError("untyped null literals are not supported")


@translate_literal.register
def _literal_boolean(
    _: dt.Boolean,
    value: bool,
) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(boolean=value)


@translate_literal.register
def _literal_int8(_: dt.Int8, value: int) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(i8=value)


@translate_literal.register
def _literal_int16(_: dt.Int16, value: int) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(i16=value)


@translate_literal.register
def _literal_int32(_: dt.Int32, value: int) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(i32=value)


@translate_literal.register
def _literal_int64(_: dt.Int64, value: int) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(i64=value)


@translate_literal.register
def _literal_float32(_: dt.Float32, value: float) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(fp32=value)


@translate_literal.register
def _literal_float64(_: dt.Float64, value: float) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(fp64=value)


@translate_literal.register
def _literal_string(_: dt.String, value: str) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(string=value)


@translate_literal.register
def _literal_binary(_: dt.Binary, value: bytes) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(binary=value)


@translate_literal.register
def _literal_timestamp(
    dtype: dt.Timestamp,
    value: datetime.datetime,
) -> stexpr.Expression.Literal:
    micros_since_epoch = int(value.timestamp() * 1e6)
    if dtype.timezone is not None:
        return stexpr.Expression.Literal(timestamp_tz=micros_since_epoch)
    return stexpr.Expression.Literal(timestamp=micros_since_epoch)


@translate_literal.register
def _literal_struct(
    dtype: dt.Struct,
    mapping: collections.OrderedDict,
) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(
        struct=stexpr.Expression.Literal.Struct(
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
) -> stexpr.Expression.Literal:
    if not mapping:
        return stexpr.Expression.Literal(empty_map=translate(dtype).map)
    return stexpr.Expression.Literal(
        map=stexpr.Expression.Literal.Map(
            key_values=[
                stexpr.Expression.Literal.Map.KeyValue(
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
) -> stexpr.Expression.Literal:
    if not sequence:
        return stexpr.Expression.Literal(empty_list=translate(dtype).list)
    return stexpr.Expression.Literal(
        list=stexpr.Expression.Literal.List(
            values=[translate_literal(dtype.value_type, value) for value in sequence],
        )
    )


@translate_literal.register(dt.UUID)
def _literal_uuid(_: dt.UUID, value: str | uuid.UUID) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(uuid=uuid.UUID(hex=str(value)).bytes)


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
def _literal_time(time: dt.Time, value: datetime.time) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(time=_time_to_micros(value))


def _date_to_days(value: datetime.date) -> int:
    delta = value - datetime.datetime.utcfromtimestamp(0).date()
    return delta.days


@translate_literal.register
def _literal_date(date: dt.Date, value: datetime.date) -> stexpr.Expression.Literal:
    return stexpr.Expression.Literal(date=_date_to_days(value))


@functools.singledispatch
def translate_preceding(value: int | None) -> stexpr.Expression.WindowFunction.Bound:
    raise NotImplementedError()


@translate_preceding.register
def _preceding_none(_: None) -> stexpr.Expression.WindowFunction.Bound:
    return stexpr.Expression.WindowFunction.Bound(
        unbounded=stexpr.Expression.WindowFunction.Bound.Unbounded()
    )


@translate_preceding.register
def _preceding_int(offset: int) -> stexpr.Expression.WindowFunction.Bound:
    return stexpr.Expression.WindowFunction.Bound(
        preceding=stexpr.Expression.WindowFunction.Bound.Preceding(offset=offset)
    )


@functools.singledispatch
def translate_following(value: int | None) -> stexpr.Expression.WindowFunction.Bound:
    raise NotImplementedError()


@translate_following.register
def _following_none(_: None) -> stexpr.Expression.WindowFunction.Bound:
    return translate_preceding(_)


@translate_following.register
def _following_int(offset: int) -> stexpr.Expression.WindowFunction.Bound:
    return stexpr.Expression.WindowFunction.Bound(
        following=stexpr.Expression.WindowFunction.Bound.Following(offset=offset)
    )


def _translate_window_bounds(
    precedes: tuple[int, int] | int | None,
    follows: tuple[int, int] | int | None,
) -> tuple[
    stexpr.Expression.WindowFunction.Bound,
    stexpr.Expression.WindowFunction.Bound,
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


@translate.register(ops.ValueOp)
def value_op(
    op: ops.ValueOp,
    expr: ir.ValueExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stexpr.Expression:
    # given the details of `op` -> function id
    return stexpr.Expression(
        scalar_function=stexpr.Expression.ScalarFunction(
            function_reference=compiler.function_id(expr),
            output_type=translate(expr.type()),
            args=[
                translate(arg, compiler, **kwargs)
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
) -> stexpr.Expression:
    lower_bound, upper_bound = _translate_window_bounds(
        op.window.preceding, op.window.following
    )
    return stexpr.Expression(
        window_function=stexpr.Expression.WindowFunction(
            function_reference=compiler.function_id(op.expr),
            partitions=[
                translate(gb, compiler, **kwargs) for gb in op.window._group_by
            ],
            sorts=[translate(ob, compiler, **kwargs) for ob in op.window._order_by],
            output_type=translate(expr.type()),
            phase=stexpr.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
            args=[
                translate(arg, compiler, **kwargs)
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
) -> stexpr.AggregateFunction:
    return stexpr.AggregateFunction(
        function_reference=compiler.function_id(expr),
        args=[translate(op.arg, compiler, **kwargs)],
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stexpr.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(expr.type()),
    )


@translate.register(ops.Count)
def _count(
    op: ops.Count,
    expr: ir.ScalarExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stexpr.AggregateFunction:
    translated_args = []
    arg = op.arg
    if not isinstance(arg, ir.TableExpr):
        translated_args.append(translate(arg, compiler, **kwargs))
    return stexpr.AggregateFunction(
        function_reference=compiler.function_id(expr),
        args=translated_args,
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stexpr.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(expr.type()),
    )


@translate.register(ops.SortKey)
def sort_key(
    op: ops.SortKey,
    expr: ir.SortExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stexpr.SortField:
    ordering = "ASC" if op.ascending else "DESC"
    return stexpr.SortField(
        expr=translate(op.expr, compiler, **kwargs),
        direction=getattr(
            stexpr.SortField.SortDirection,
            f"SORT_DIRECTION_{ordering}_NULLS_FIRST",
        ),
    )


@translate.register(ops.TableColumn)
def table_column(
    op: ops.TableColumn,
    expr: ir.ColumnExpr,
    _: SubstraitCompiler,
    *,
    child_ordinals: MutableMapping[ops.TableNode, int] | None = None,
) -> stexpr.Expression:
    schema = op.table.schema()
    position = schema._name_locs[op.name]
    return stexpr.Expression(
        selection=stexpr.Expression.FieldReference(
            direct_reference=stexpr.Expression.ReferenceSegment(
                struct_field=stexpr.Expression.ReferenceSegment.StructField(
                    field=position,
                    child=stexpr.Expression.ReferenceSegment(
                        struct_field=stexpr.Expression.ReferenceSegment.StructField(
                            field=(child_ordinals or {}).get(op.table.op(), 0),
                        ),
                    ),
                ),
            ),
        )
    )


@translate.register(ops.UnboundTable)
def unbound_table(
    op: ops.UnboundTable, expr: ir.TableExpr, _: SubstraitCompiler, **kwargs: Any
) -> strel.Rel:
    return strel.Rel(
        read=strel.ReadRel(
            # TODO: filter,
            # TODO: projection,
            base_schema=translate(op.schema),
            named_table=strel.ReadRel.NamedTable(names=[op.name]),
        )
    )


def _get_child_ordinals(table: ir.TableExpr) -> dict[ops.TableNode, int]:
    table_op = table.op()
    if isinstance(table_op, ops.Join):
        return {t: i for i, t in enumerate(table_op.root_tables())}
    return {}


@translate.register(ops.Selection)
def selection(
    op: ops.Selection,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> strel.Rel:
    assert not kwargs.get(
        "child_ordinals"
    ), "non-None child_ordinals passed in to selection translation rule"
    child_ordinals = _get_child_ordinals(op.table)
    # source
    relation = translate(
        op.table,
        compiler,
        child_ordinals=child_ordinals,
    )

    # filter
    if op.predicates:
        relation = strel.Rel(
            filter=strel.FilterRel(
                input=relation,
                condition=translate(
                    functools.reduce(operator.and_, op.predicates),
                    compiler,
                    child_ordinals=child_ordinals,
                ),
            )
        )

    # projection
    if op.selections:
        relation = strel.Rel(
            project=strel.ProjectRel(
                input=relation,
                expressions=[
                    translate(selection, compiler, child_ordinals=child_ordinals)
                    for selection in op.selections
                ],
            )
        )

    # order by
    if op.sort_keys:
        relation = strel.Rel(
            sort=strel.SortRel(
                input=relation,
                sorts=[
                    translate(key, compiler, child_ordinals=child_ordinals)
                    for key in op.sort_keys
                ],
            )
        )

    return relation


@functools.singledispatch
def _translate_join_type(op: ops.Join) -> strel.JoinRel.JoinType.V:
    raise NotImplementedError(f"join type `{type(op).__name__}` not implemented")


@_translate_join_type.register(ops.InnerJoin)
def _translate_inner_join(_: ops.InnerJoin) -> strel.JoinRel.JoinType.V:
    return strel.JoinRel.JoinType.JOIN_TYPE_INNER


@_translate_join_type.register(ops.OuterJoin)
def _translate_outer_join(_: ops.OuterJoin) -> strel.JoinRel.JoinType.V:
    return strel.JoinRel.JoinType.JOIN_TYPE_OUTER


@_translate_join_type.register(ops.LeftJoin)
def _translate_left_join(_: ops.LeftJoin) -> strel.JoinRel.JoinType.V:
    return strel.JoinRel.JoinType.JOIN_TYPE_LEFT


@_translate_join_type.register(ops.RightJoin)
def _translate_right_join(_: ops.RightJoin) -> strel.JoinRel.JoinType.V:
    return strel.JoinRel.JoinType.JOIN_TYPE_RIGHT


@_translate_join_type.register(ops.LeftSemiJoin)
def _translate_semi_join(_: ops.LeftSemiJoin) -> strel.JoinRel.JoinType.V:
    return strel.JoinRel.JoinType.JOIN_TYPE_SEMI


@_translate_join_type.register(ops.LeftAntiJoin)
def _translate_anti_join(_: ops.LeftAntiJoin) -> strel.JoinRel.JoinType.V:
    return strel.JoinRel.JoinType.JOIN_TYPE_ANTI


@translate.register(ops.Join)
def join(
    op: ops.Join,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> strel.Rel:
    child_ordinals = _get_child_ordinals(expr)
    return strel.Rel(
        join=strel.JoinRel(
            left=translate(op.left, compiler, **kwargs),
            right=translate(op.right, compiler, **kwargs),
            expression=translate(
                functools.reduce(operator.and_, op.predicates),
                compiler,
                child_ordinals=child_ordinals,
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
) -> strel.Rel:
    return strel.Rel(
        fetch=strel.FetchRel(
            input=translate(op.table, compiler),
            offset=op.offset,
            count=op.n,
        )
    )


@functools.singledispatch
def translate_set_op_type(op: ops.SetOp) -> strel.SetRel.SetOp.V:
    raise NotImplementedError(
        f"set operation `{type(op).__name__}` not yet implemented"
    )


@translate_set_op_type.register(ops.Union)
def set_op_type_union(op: ops.Union) -> strel.SetRel.SetOp.V:
    if op.distinct:
        return strel.SetRel.SetOp.SET_OP_UNION_DISTINCT
    return strel.SetRel.SetOp.SET_OP_UNION_ALL


@translate_set_op_type.register(ops.Intersection)
def set_op_type_intersection(op: ops.Intersection) -> strel.SetRel.SetOp.V:
    return strel.SetRel.SetOp.SET_OP_INTERSECTION_PRIMARY


@translate_set_op_type.register(ops.Difference)
def set_op_type_difference(op: ops.Difference) -> strel.SetRel.SetOp.V:
    return strel.SetRel.SetOp.SET_OP_MINUS_PRIMARY


@translate.register(ops.SetOp)
def set_op(
    op: ops.SetOp,
    expr: ir.TableExpr,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> strel.Rel:
    return strel.Rel(
        set=strel.SetRel(
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
) -> strel.Rel:
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
        input = strel.Rel(sort=strel.SortRel(input=input, sorts=sorts))

    aggregate = strel.AggregateRel(
        input=input,
        groupings=[
            strel.AggregateRel.Grouping(
                grouping_expressions=[translate(by, compiler, **kwargs)]
            )
            for by in op.by
        ],
        measures=[
            strel.AggregateRel.Measure(measure=translate(metric, compiler, **kwargs))
            for metric in op.metrics
        ],
    )

    return strel.Rel(aggregate=aggregate)
