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
from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from typing import Any, TypeVar, Union

import ibis
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.schema as sch
import ibis.expr.types as ir
from ibis import util
from substrait.gen.proto import algebra_pb2 as stalg
from substrait.gen.proto import type_pb2 as stt

from ibis_substrait.compiler.core import SubstraitCompiler, _get_fields
from ibis_substrait.compiler.mapping import (
    IBIS_SUBSTRAIT_OP_MAPPING,
    _extension_mapping,
)

try:
    from typing import TypeAlias
except ImportError:
    # Python <= 3.9
    from typing_extensions import TypeAlias


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
    unit = dtype.unit.name
    nullability = _nullability(dtype)

    if unit == "YEAR":
        return stt.Type(interval_year=stt.Type.IntervalYear(nullability=nullability))
    elif unit == "MONTH":
        return stt.Type(interval_year=stt.Type.IntervalYear(nullability=nullability))
    elif unit == "DAY":
        return stt.Type(interval_day=stt.Type.IntervalDay(nullability=nullability))
    elif unit == "SECOND":
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
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return translate(expr.op(), compiler=compiler, **kwargs)


@translate.register(ops.Literal)
def _literal(
    op: ops.Literal,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    if op.value is None:
        return stalg.Expression(
            literal=stalg.Expression.Literal(null=translate(op.dtype, **kwargs))  # type: ignore
        )
    return stalg.Expression(literal=translate_literal(op.dtype, op.value))  # type: ignore


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


@translate_following.register
@translate_preceding.register
def _window_boundary(  # type: ignore
    boundary: ops.window.WindowBoundary,
) -> stalg.Expression.WindowFunction.Bound:
    # new window boundary class in Ibis 5.x
    if boundary.preceding:
        return translate_preceding(boundary.value.value)  # type: ignore
    else:
        return translate_following(boundary.value.value)  # type: ignore


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

    # Change in behavior of `promote_list` in Ibis 4.x so we do this for now
    preceding = [None] if precedes is None else preceding
    following = [None] if follows is None else following

    if len(preceding) == 2:
        if following and following != [None]:
            raise ValueError(
                "`following` not allowed when window bounds are both preceding"
            )

        lower, upper = preceding
        return translate_preceding(lower), translate_preceding(upper)

    if len(preceding) != 1:
        raise ValueError(f"preceding must be length 1 or 2 got: {len(preceding)}")

    if len(following) == 2:
        if preceding and preceding != [None]:
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
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # For an alias, dispatch on the underlying argument
    return translate(op.arg, compiler=compiler, **kwargs)


@translate.register(ops.ValueOp)  # type: ignore
def value_op(
    op: ops.ValueOp,  # type: ignore
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # Check if scalar function is valid for input dtype(s) and insert casts as needed to
    # make sure inputs are correct.
    op = _check_and_upcast(op)
    # given the details of `op` -> function id
    return stalg.Expression(
        scalar_function=stalg.Expression.ScalarFunction(
            function_reference=compiler.function_id(op),
            output_type=translate(op.dtype),
            arguments=[
                stalg.FunctionArgument(
                    value=translate(arg, compiler=compiler, **kwargs)
                )
                for arg in op.args
                if isinstance(arg, ops.Value)
            ],
        )
    )


@translate.register(ops.WindowOp)  # type: ignore
def window_op(
    op: ops.WindowOp,  # type: ignore
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    window_gb = op.group_by
    window_ob = op.order_by
    start = op.start
    end = op.end
    func = op.func
    func_args = op.func.args

    lower_bound, upper_bound = _translate_window_bounds(start, end)

    return stalg.Expression(
        window_function=stalg.Expression.WindowFunction(
            function_reference=compiler.function_id(func),
            partitions=[translate(gb, compiler=compiler, **kwargs) for gb in window_gb],
            sorts=[translate(ob, compiler=compiler, **kwargs) for ob in window_ob],
            output_type=translate(op.dtype),
            phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
            arguments=[
                stalg.FunctionArgument(
                    value=translate(arg, compiler=compiler, **kwargs)
                )
                for arg in func_args
                if isinstance(arg, ops.Value)
            ],
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )
    )


@translate.register(ops.Reduction)
def _reduction(
    op: ops.Reduction,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.AggregateFunction:
    return stalg.AggregateFunction(
        function_reference=compiler.function_id(op),
        arguments=[
            stalg.FunctionArgument(value=translate(op.arg, compiler=compiler, **kwargs))  # type: ignore
        ],
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(op.dtype),
    )


@translate.register(ops.CountDistinct)
def _count_distinct(
    op: ops.Count,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.AggregateFunction:
    translated_args: list[stalg.FunctionArgument] = []
    if not isinstance(op.arg, ops.Relation):
        translated_args.append(
            stalg.FunctionArgument(value=translate(op.arg, compiler=compiler, **kwargs))
        )
    return stalg.AggregateFunction(
        function_reference=compiler.function_id(op),
        arguments=translated_args,
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(op.dtype),
        invocation=stalg.AggregateFunction.AGGREGATION_INVOCATION_DISTINCT,
    )


@translate.register(ops.Count)
@translate.register(ops.CountStar)
def _count(
    op: ops.Count,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.AggregateFunction:
    translated_args: list[stalg.FunctionArgument] = []
    if not isinstance(op.arg, ops.Relation):
        translated_args.append(
            stalg.FunctionArgument(value=translate(op.arg, compiler=compiler, **kwargs))
        )
    return stalg.AggregateFunction(
        function_reference=compiler.function_id(op),
        arguments=translated_args,
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(op.dtype),
    )


@translate.register(ops.StandardDev)
@translate.register(ops.Variance)
def _variance_base(
    op: ops.StandardDev | ops.Variance,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.AggregateFunction:
    translated_arg = stalg.FunctionArgument(
        value=translate(op.arg, compiler=compiler, **kwargs)
    )
    translated_how = stalg.FunctionOption(
        name="distribution", preference=["POPULATION" if op.how == "pop" else "SAMPLE"]
    )
    return stalg.AggregateFunction(
        function_reference=compiler.function_id(op=op),
        arguments=[translated_arg],
        options=[translated_how],
        sorts=[],  # TODO: ibis doesn't support this yet
        phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
        output_type=translate(op.dtype),
    )


@translate.register(ops.SortKey)
def sort_key(
    op: ops.SortKey,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.SortField:
    ordering = "ASC" if op.ascending else "DESC"
    return stalg.SortField(
        expr=translate(op.expr, compiler=compiler, **kwargs),
        direction=getattr(
            stalg.SortField.SortDirection,
            f"SORT_DIRECTION_{ordering}_NULLS_FIRST",
        ),
    )


@translate.register(ops.Field)
def table_column(
    op: ops.Field,
    *,
    compiler: SubstraitCompiler,
    child_rel_field_offsets: MutableMapping[ops.TableNode, int] | None = None,
    **kwargs: Any,
) -> stalg.Expression:
    if child_rel_field_offsets and isinstance(op.rel, ops.JoinReference):
        base_offset = child_rel_field_offsets.get(op.rel, 0)
    else:
        base_offset = 0

    if isinstance(op.rel, ops.JoinChain):
        # JoinChains provide the schema of the joined table (which is great for Ibis)
        # but for substrait we need the Field index computed with respect to
        # the original table schemas.  In practice, this means rolling through
        # the tables in a JoinChain and computing the field index _without_
        # removing the join key
        #
        # Given
        # Table 1
        #   a: int
        #   b: int
        #
        # Table 2
        #   a: int
        #   c: int
        #
        # JoinChain[r0]
        #  JoinLink[inner, r1]
        #    r0.a == r1.a
        #  values:
        #    a: r0.a
        #    b: r0.b
        #    c: r1.c
        #
        # If we ask for the field index of `c`, the JoinChain schema will give
        # us an index of `2`, but it should be `3` because
        #
        #  0: table 1 a
        #  1: table 1 b
        #  2: table 2 a
        #  3: table 2 c
        #

        # List of join reference objects
        join_tables = op.rel.tables
        # Join reference containing the field we care about
        field_table = op.rel.values.get(op.name).rel
        # Index of that join reference in the list of join references
        field_table_index = join_tables.index(field_table)

        # Offset by the number of columns in each preceding table
        join_table_offset = sum(
            len(join_tables[i].schema) for i in range(field_table_index)
        )
        # Then add on the index of the column in the table
        # Also in the event of renaming due to join collisions, resolve
        # the renamed column to the original name so we can pull it off the parent table
        orig_name = op.rel.values[op.name].name
        relative_offset = join_table_offset + field_table.schema._name_locs[orig_name]
    else:
        schema = op.rel.schema
        relative_offset = schema._name_locs[op.name]
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
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    child = translate(op.arg, compiler=compiler, **kwargs)
    field_name = op.field
    # TODO: store names/types inverse mapping on datatypes.Struct for O(1)
    # access to field index
    field_index = op.arg.dtype.names.index(field_name)

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
    op: ops.UnboundTable,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
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


@translate.register(ops.Filter)
def filter(
    filter: ops.Filter,
    *,
    compiler: SubstraitCompiler,
    child_rel_field_offsets: Mapping[ops.TableNode, int] | None = None,
    **kwargs: Any,
) -> stalg.Rel:
    relation = translate(
        filter.parent,
        compiler=compiler,
        child_rel_field_offsets=child_rel_field_offsets,
    )
    predicates = [pred.to_expr() for pred in filter.predicates]  # type: ignore
    return stalg.Rel(
        filter=stalg.FilterRel(
            input=relation,
            condition=translate(
                functools.reduce(operator.and_, predicates),
                compiler=compiler,
                child_rel_field_offsets=child_rel_field_offsets,
                **kwargs,
            ),
        )
    )


@translate.register(ops.Project)
def project(
    op: ops.Project,
    *,
    compiler: SubstraitCompiler,
    child_rel_field_offsets: Mapping[ops.TableNode, int] | None = None,
    **kwargs: Any,
) -> stalg.Rel:
    relation = translate(
        op.parent, compiler=compiler, child_rel_field_offsets=child_rel_field_offsets
    )
    mapping_counter = itertools.count(len(op.parent.schema))

    return stalg.Rel(
        project=stalg.ProjectRel(
            input=relation,
            common=stalg.RelCommon(
                emit=stalg.RelCommon.Emit(
                    output_mapping=[next(mapping_counter) for _ in op.values]
                )
            ),
            expressions=[
                translate(
                    v,
                    compiler=compiler,
                    child_rel_field_offsets=child_rel_field_offsets,
                    **kwargs,
                )
                for k, v in op.values.items()
            ],
        )
    )


@translate.register(ops.Sort)
def sort(
    op: ops.Sort,
    *,
    compiler: SubstraitCompiler,
    child_rel_field_offsets: Mapping[ops.TableNode, int] | None = None,
    **kwargs: Any,
) -> stalg.Rel:
    relation = translate(
        op.parent, compiler=compiler, child_rel_field_offsets=child_rel_field_offsets
    )

    return stalg.Rel(
        sort=stalg.SortRel(
            input=relation,
            sorts=[
                translate(
                    key,
                    compiler=compiler,
                    child_rel_field_offsets=child_rel_field_offsets,
                    **kwargs,
                )
                for key in op.keys
            ],
        )
    )


def _translate_join_type(join_kind: ops.JoinKind) -> stalg.JoinRel.JoinType.V:
    JOIN_KIND_MAP = {
        "inner": stalg.JoinRel.JoinType.JOIN_TYPE_INNER,
        "left": stalg.JoinRel.JoinType.JOIN_TYPE_LEFT,
        "right": stalg.JoinRel.JoinType.JOIN_TYPE_RIGHT,
        "outer": stalg.JoinRel.JoinType.JOIN_TYPE_OUTER,
        "semi": stalg.JoinRel.JoinType.JOIN_TYPE_SEMI,
        # "asof",
        # "anti",
        # "any_inner",
        # "any_left",
        # "cross"
    }
    return JOIN_KIND_MAP[join_kind]


@translate.register(ops.JoinChain)
def join(
    op: ops.JoinChain,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    child_rel_field_offsets = kwargs.pop("child_rel_field_offsets", None)
    if not child_rel_field_offsets:
        child_rel_field_offsets = {}
        child_rel_field_offsets[op.first] = 0
        offset = len(op.first.parent.schema)
        for join_link in op.rest:
            child_rel_field_offsets[join_link.table] = offset
            offset += len(join_link.table.schema)

    relation = None

    for i, join_link in enumerate(op.rest):
        predicates = [pred.to_expr() for pred in join_link.predicates]

        relation = stalg.Rel(
            join=stalg.JoinRel(
                left=(
                    translate(op.first.parent, compiler=compiler, **kwargs)
                    if i == 0
                    else relation
                ),
                right=translate(join_link.table.parent, compiler=compiler, **kwargs),
                expression=translate(
                    functools.reduce(operator.and_, predicates),
                    compiler=compiler,
                    child_rel_field_offsets=child_rel_field_offsets,
                    **kwargs,
                ),
                type=_translate_join_type(join_link.how),
            )
        )

    return relation


@translate.register(ops.Limit)
def limit(
    op: ops.Limit,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    return stalg.Rel(
        fetch=stalg.FetchRel(
            input=translate(op.parent, compiler=compiler, **kwargs),
            offset=op.offset,
            count=op.n,
        )
    )


@functools.singledispatch
def translate_set_op_type(op: ops.Union) -> stalg.SetRel.SetOp.V:
    raise NotImplementedError(
        f"set operation `{type(op).__name__}` not yet implemented"
    )


@translate_set_op_type.register(ops.Union)  # type: ignore
def set_op_type_union(op: ops.Union) -> stalg.SetRel.SetOp.V:
    if op.distinct:  # type: ignore
        return stalg.SetRel.SetOp.SET_OP_UNION_DISTINCT
    return stalg.SetRel.SetOp.SET_OP_UNION_ALL


@translate_set_op_type.register(ops.Intersection)
def set_op_type_intersection(op: ops.Intersection) -> stalg.SetRel.SetOp.V:
    return stalg.SetRel.SetOp.SET_OP_INTERSECTION_PRIMARY


@translate_set_op_type.register(ops.Difference)
def set_op_type_difference(op: ops.Difference) -> stalg.SetRel.SetOp.V:
    return stalg.SetRel.SetOp.SET_OP_MINUS_PRIMARY


@translate.register(ops.Set)
def set_op(
    op: ops.Set,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    return stalg.Rel(
        set=stalg.SetRel(
            inputs=[
                translate(op.left, compiler=compiler, **kwargs),
                translate(op.right, compiler=compiler, **kwargs),
            ],
            op=translate_set_op_type(op),
        )
    )


@translate.register(ops.Aggregate)
def aggregate(
    op: ops.Aggregate,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Rel:
    aggregate = stalg.AggregateRel(
        input=translate(op.parent, compiler=compiler, **kwargs),
        groupings=[
            stalg.AggregateRel.Grouping(
                grouping_expressions=[
                    translate(group, compiler=compiler, **kwargs)
                    for group in op.groups.values()
                ]
            )
        ],
        measures=[
            stalg.AggregateRel.Measure(
                measure=translate(agg_func, compiler=compiler, **kwargs)
            )
            for agg_func in op.metrics.values()
        ],
    )

    return stalg.Rel(aggregate=aggregate)


@translate.register(ops.SimpleCase)
@translate.register(ops.SearchedCase)
def _simple_searched_case(
    op: ops.SimpleCase | ops.SearchedCase,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # the field names for an `if_then` are `if` and `else` which means we need
    # to pass those args in as a dictionary to not run afoul of SyntaxErrors`
    _ifs = []
    for case, result in zip(op.cases, op.results):
        if_expr = case if not hasattr(op, "base") else op.base.to_expr() == case
        _if = {
            "if": translate(if_expr, compiler=compiler, **kwargs),
            "then": translate(result, compiler=compiler, **kwargs),
        }
        _ifs.append(stalg.Expression.IfThen.IfClause(**_if))

    _else = {"else": translate(op.default, compiler=compiler, **kwargs)}

    return stalg.Expression(if_then=stalg.Expression.IfThen(ifs=_ifs, **_else))


@translate.register(ops.IfElse)
def _where(
    op: ops.IfElse,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # the field names for an `if_then` are `if` and `else` which means we need
    # to pass those args in as a dictionary to not run afoul of SyntaxErrors`
    _if = {
        "if": translate(op.bool_expr, compiler=compiler, **kwargs),
        "then": translate(op.true_expr, compiler=compiler, **kwargs),
    }
    _else = {"else": translate(op.false_null_expr, compiler=compiler, **kwargs)}

    _ifs = [stalg.Expression.IfThen.IfClause(**_if)]

    return stalg.Expression(if_then=stalg.Expression.IfThen(ifs=_ifs, **_else))


@translate.register(ops.InValues)  # type: ignore
def _contains(
    op: ops.InValues,  # type: ignore
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    options = (
        op.options
        if isinstance(op.options, Iterable)
        else ibis.util.promote_list(op.options)
    )
    return stalg.Expression(
        singular_or_list=stalg.Expression.SingularOrList(
            value=translate(op.value, compiler=compiler, **kwargs),
            options=[
                translate(value, compiler=compiler, **kwargs) for value in options
            ],
        )
    )


@translate.register(ops.Cast)
def _cast(
    op: ops.Cast,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return stalg.Expression(
        cast=stalg.Expression.Cast(
            type=translate(op.to),
            input=translate(op.arg, compiler=compiler, **kwargs),
            failure_behavior=stalg.Expression.Cast.FAILURE_BEHAVIOR_THROW_EXCEPTION,
        )
    )


@translate.register(ops.ExtractDateField)
def _extractdatefield(
    op: ops.ExtractDateField,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    # e.g. "ExtractYear" -> "YEAR"
    span = type(op).__name__[len("Extract") :].upper()
    arguments = (
        stalg.FunctionArgument(value=translate(arg, compiler=compiler, **kwargs))
        for arg in op.args
        if isinstance(arg, ops.Value)
    )
    scalar_func = stalg.Expression.ScalarFunction(
        function_reference=compiler.function_id(op),
        output_type=translate(op.dtype),
    )
    scalar_func.arguments.add(enum=span)
    scalar_func.arguments.extend(arguments)
    return stalg.Expression(scalar_function=scalar_func)


@translate.register(ops.Log)
def _log(
    op: ops.Log,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    arg = stalg.FunctionArgument(value=translate(op.arg, compiler=compiler, **kwargs))
    base = stalg.FunctionArgument(
        value=translate(
            op.base if op.base is not None else ibis.literal(math.e),
            compiler=compiler,
            **kwargs,
        )
    )

    scalar_func = stalg.Expression.ScalarFunction(
        function_reference=compiler.function_id(op),
        output_type=translate(op.dtype),
        arguments=[arg, base],
    )
    return stalg.Expression(scalar_function=scalar_func)


@translate.register(ops.FloorDivide)
def _floordivide(
    op: ops.FloorDivide,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    left, right = op.left, op.right
    return translate((left / right).floor(), compiler=compiler, **kwargs)  # type: ignore


@translate.register(ops.Clip)
def _clip(
    op: ops.Clip,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    arg, lower, upper = op.arg, op.lower, op.upper

    if lower is not None and upper is not None:
        return translate(
            (arg >= lower).ifelse((arg <= upper).ifelse(arg, upper), lower),  # type: ignore
            compiler=compiler,
            **kwargs,
        )
    elif lower is not None:
        return translate(
            (arg >= lower).ifelse(arg, lower),  # type: ignore
            compiler=compiler,
            **kwargs,
        )
    elif upper is not None:
        return translate(
            (arg <= upper).ifelse(arg, upper),  # type: ignore
            compiler=compiler,
            **kwargs,
        )
    raise AssertionError()


@translate.register(ops.SelfReference)
def _self_reference(
    op: ops.SelfReference,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return translate(op.parent, compiler=compiler, **kwargs)


@translate.register(ops.ScalarSubquery)
def _scalar_subquery(
    op: ops.ScalarSubquery,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return stalg.Expression(
        subquery=stalg.Expression.Subquery(
            scalar=stalg.Expression.Subquery.Scalar(
                input=translate(op.rel, compiler=compiler)
            )
        )
    )


@translate.register(ops.InSubquery)
def _in_subquery(
    op: ops.InSubquery,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return stalg.Expression(
        subquery=stalg.Expression.Subquery(
            in_predicate=stalg.Expression.Subquery.InPredicate(
                needles=[translate(op.needle, compiler=compiler)],
                haystack=translate(op.rel, compiler=compiler),
            )
        )
    )


@translate.register(ops.ExistsSubquery)
def _exists_subquery(
    op: ops.ExistsSubquery,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    return stalg.Expression(
        subquery=stalg.Expression.Subquery(
            set_predicate=stalg.Expression.Subquery.SetPredicate(
                predicate_op=stalg.Expression.Subquery.SetPredicate.PREDICATE_OP_EXISTS,
                tuples=translate(op.rel, compiler=compiler),
            )
        )
    )


def _not_exists_subquery(
    op: ops.NotExistsSubquery,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    assert compiler is not None
    tuples = stalg.Rel(
        filter=stalg.FilterRel(
            input=translate(op.foreign_table, compiler=compiler),
            condition=translate(
                functools.reduce(ops.And, op.predicates),  # type: ignore
                compiler=compiler,
                **kwargs,
            ),
        )
    )

    return stalg.Expression(
        scalar_function=stalg.Expression.ScalarFunction(
            function_reference=compiler.function_id(ops.Not(op)),  # type: ignore
            output_type=translate(op.dtype),
            arguments=[
                stalg.FunctionArgument(
                    value=stalg.Expression(
                        subquery=stalg.Expression.Subquery(
                            set_predicate=stalg.Expression.Subquery.SetPredicate(
                                predicate_op=stalg.Expression.Subquery.SetPredicate.PREDICATE_OP_EXISTS,
                                tuples=tuples,
                            )
                        )
                    )
                )
            ],
        )
    )


@translate.register(ops.Floor)
@translate.register(ops.Ceil)
def _floor_ceil_cast(
    op: ops.Floor,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    output_type = translate(op.dtype)
    input = stalg.Expression(
        scalar_function=stalg.Expression.ScalarFunction(
            function_reference=compiler.function_id(op),
            output_type=output_type,
            arguments=[
                stalg.FunctionArgument(
                    value=translate(arg, compiler=compiler, **kwargs)
                )
                for arg in op.func_args  # type: ignore
                if isinstance(arg, ops.Value)
            ],
        )
    )
    return stalg.Expression(
        cast=stalg.Expression.Cast(
            type=output_type,
            input=input,
            failure_behavior=stalg.Expression.Cast.FAILURE_BEHAVIOR_THROW_EXCEPTION,
        )
    )


@translate.register(ops.ElementWiseVectorizedUDF)
def _elementwise_udf(
    op: ops.ElementWiseVectorizedUDF,
    *,
    compiler: SubstraitCompiler,
    **kwargs: Any,
) -> stalg.Expression:
    if compiler.udf_uri is None:
        raise ValueError(
            """
Cannot compile a Substrait plan that contains a UDF unless the
compiler has a `udf_uri` attached.
        """
        )

    # For referring to scalar function within plan use "{op_name}_{udf_name}"
    # since op_name alone will collide with >1 UDF
    udf_key = f"{type(op).__name__}_{op.func.__name__}"

    # Explicitly register extension uri
    extension_uri = compiler.register_extension_uri(compiler.udf_uri)

    # Explicitly register extension function
    try:
        func_ext = compiler.function_extensions[udf_key]
    except KeyError:
        func_ext = compiler.function_extensions[udf_key] = (
            compiler.create_extension_function(extension_uri, op.func.__name__)
        )

    return stalg.Expression(
        scalar_function=stalg.Expression.ScalarFunction(
            function_reference=func_ext.function_anchor,
            output_type=translate(op.return_type),
            arguments=[
                stalg.FunctionArgument(
                    value=translate(arg, compiler=compiler, **kwargs)
                )
                for arg in op.func_args
                if isinstance(arg, ops.Value)
            ],
        )
    )


def _check_and_upcast(op: ops.Node) -> ops.Node:
    """Check that arguments to extension functions have consistent types."""
    op_name = IBIS_SUBSTRAIT_OP_MAPPING[type(op).__name__]
    anykey = ("any",) * len([arg for arg in op.args if arg is not None])

    # First check if `any` is an option
    function_extension = _extension_mapping[op_name].get(anykey)

    # Otherwise, if the types don't match, cast up
    if function_extension is None:
        op = _upcast(op)

    return op


@functools.singledispatch
def _upcast(op: ops.Node) -> Any:
    return op


@_upcast.register(ops.Binary)
def _upcast_bin_op(op: ops.Binary) -> ops.Binary:
    left, right = op.left.dtype, op.right.dtype

    if left == right:
        return op
    elif dt.castable(left, right):
        return type(op)(ops.Cast(op.left, to=right), op.right)  # type: ignore
    elif dt.castable(right, left):
        return type(op)(op.left, ops.Cast(op.right, to=left))  # type: ignore
    else:
        raise TypeError(
            f"binop {type(op).__name__} called with incompatible types {left=} {right=}"
        )


string_op: TypeAlias = Union[
    ops.Substring, ops.StrRight, ops.Repeat, ops.StringFind, ops.LPad, ops.RPad
]


@_upcast.register(ops.Substring)
@_upcast.register(ops.StrRight)
@_upcast.register(ops.Repeat)
@_upcast.register(ops.StringFind)
@_upcast.register(ops.LPad)
@_upcast.register(ops.RPad)
def _upcast_string_op(op: string_op) -> string_op:
    # Substrait wants Int32 for all numeric args to string functions
    casted_args = [
        (
            ops.Cast(newop, to=dt.Int32())  # type: ignore
            if isinstance(newop.dtype, dt.SignedInteger)
            else newop
        )
        for newop in op.args
    ]
    return type(op)(*casted_args)


@_upcast.register(ops.Round)
def _upcast_round_digits(op: ops.Round) -> ops.Round:
    # Substrait wants Int32 for decimal place argument to round
    if op.digits is None:
        raise ValueError(
            "Substrait requires that a rounding operation specify the number of digits to round to"
        )
    elif not isinstance(op.digits.dtype, dt.Int32):
        return ops.Round(
            op.arg, op.digits.copy(dtype=dt.Int32(nullable=op.digits.dtype.nullable))
        )
    return op
