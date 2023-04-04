from __future__ import annotations

import collections
import collections.abc
import datetime
import decimal
import functools
import itertools
import math
import uuid
from typing import Any, Iterable, MutableMapping, Sequence, TypeVar

import ibis
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.schema as sch
import ibis.expr.types as ir
import toolz

from ibis_substrait.compiler.core import SubstraitCompiler, _get_fields
from ibis_substrait.proto.substrait.ibis import algebra_pb2 as stalg
from ibis_substrait.proto.substrait.ibis import type_pb2 as stt

T = TypeVar("T")


def _nullability(dtype: dt.DataType) -> stt.Type.Nullability.V:
    return (
        stt.Type.Nullability.NULLABILITY_NULLABLE
        if dtype.nullable
        else stt.Type.Nullability.NULLABILITY_REQUIRED
    )


_MINUTES_PER_HOUR = _SECONDS_PER_MINUTE = 60
_MICROSECONDS_PER_SECOND = 1_000_000


def _date_to_days(value: datetime.date) -> int:
    delta = value - datetime.datetime.utcfromtimestamp(0).date()
    return delta.days


def _time_to_micros(value: datetime.time) -> int:
    """Convert a Python ``datetime.time`` object to microseconds since day-start."""
    return (
        value.hour * _MINUTES_PER_HOUR * _SECONDS_PER_MINUTE * _MICROSECONDS_PER_SECOND
        + value.minute * _SECONDS_PER_MINUTE * _MICROSECONDS_PER_SECOND
        + value.second * _MICROSECONDS_PER_SECOND
        + value.microsecond
    )


class IbisTranslator:
    def __init__(self, compiler: SubstraitCompiler) -> None:
        self.compiler = compiler

    @functools.singledispatchmethod
    def translate(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError(*args)

    @translate.register
    def _null_literal(self, _: dt.Null, **kwargs: Any) -> stalg.Expression.Literal:
        raise NotImplementedError("untyped null literals are not supported")

    @translate.register
    def _boolean(self, dtype: dt.Boolean) -> stt.Type:
        return stt.Type(bool=stt.Type.Boolean(nullability=_nullability(dtype)))

    @translate.register
    def _i8(self, dtype: dt.Int8) -> stt.Type:
        return stt.Type(i8=stt.Type.I8(nullability=_nullability(dtype)))

    @translate.register
    def _i16(self, dtype: dt.Int16) -> stt.Type:
        return stt.Type(i16=stt.Type.I16(nullability=_nullability(dtype)))

    @translate.register
    def _i32(self, dtype: dt.Int32) -> stt.Type:
        return stt.Type(i32=stt.Type.I32(nullability=_nullability(dtype)))

    @translate.register
    def _i64(self, dtype: dt.Int64) -> stt.Type:
        return stt.Type(i64=stt.Type.I64(nullability=_nullability(dtype)))

    @translate.register
    def _float32(self, dtype: dt.Float32) -> stt.Type:
        return stt.Type(fp32=stt.Type.FP32(nullability=_nullability(dtype)))

    @translate.register
    def _float64(self, dtype: dt.Float64) -> stt.Type:
        return stt.Type(fp64=stt.Type.FP64(nullability=_nullability(dtype)))

    @translate.register
    def _string(self, dtype: dt.String) -> stt.Type:
        return stt.Type(string=stt.Type.String(nullability=_nullability(dtype)))

    @translate.register
    def _binary(self, dtype: dt.Binary) -> stt.Type:
        return stt.Type(binary=stt.Type.Binary(nullability=_nullability(dtype)))

    @translate.register
    def _date(self, dtype: dt.Date) -> stt.Type:
        return stt.Type(date=stt.Type.Date(nullability=_nullability(dtype)))

    @translate.register
    def _time(self, dtype: dt.Time) -> stt.Type:
        return stt.Type(time=stt.Type.Time(nullability=_nullability(dtype)))

    @translate.register
    def _decimal(self, dtype: dt.Decimal) -> stt.Type:
        return stt.Type(
            decimal=stt.Type.Decimal(
                scale=dtype.scale,
                precision=dtype.precision,
                nullability=_nullability(dtype),
            )
        )

    @translate.register
    def _timestamp(self, dtype: dt.Timestamp) -> stt.Type:
        nullability = _nullability(dtype)
        if dtype.timezone is not None:
            return stt.Type(timestamp_tz=stt.Type.TimestampTZ(nullability=nullability))
        return stt.Type(timestamp=stt.Type.Timestamp(nullability=nullability))

    @translate.register
    def _interval(self, dtype: dt.Interval) -> stt.Type:
        unit = dtype.unit
        nullability = _nullability(dtype)

        if unit == "Y":
            return stt.Type(
                interval_year=stt.Type.IntervalYear(nullability=nullability)
            )
        elif unit == "M":
            return stt.Type(
                interval_year=stt.Type.IntervalYear(nullability=nullability)
            )
        elif unit == "D":
            return stt.Type(interval_day=stt.Type.IntervalDay(nullability=nullability))
        elif unit == "s":
            return stt.Type(interval_day=stt.Type.IntervalDay(nullability=nullability))

        raise ValueError(f"unsupported substrait unit: {unit!r}")

    @translate.register
    def _array(self, dtype: dt.Array) -> stt.Type:
        return stt.Type(
            list=stt.Type.List(
                type=self.translate(dtype.value_type),
                nullability=_nullability(dtype),
            )
        )

    @translate.register
    def _map(self, dtype: dt.Map) -> stt.Type:
        return stt.Type(
            map=stt.Type.Map(
                key=self.translate(dtype.key_type),
                value=self.translate(dtype.value_type),
                nullability=_nullability(dtype),
            )
        )

    def _struct(
        self,
        struct: dt.Struct,
        *,
        nullability: stt.Type.Nullability.V,
    ) -> stt.Type.Struct:
        return stt.Type.Struct(
            types=list(map(self.translate, struct.types)),
            nullability=nullability,
        )

    @translate.register
    def _struct_type(self, dtype: dt.Struct) -> stt.Type:
        return stt.Type(struct=self._struct(dtype, nullability=_nullability(dtype)))

    @translate.register
    def _schema(self, schema: sch.Schema) -> stt.NamedStruct:
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
                types=list(map(self.translate, schema.types)),
                nullability=stt.Type.Nullability.NULLABILITY_REQUIRED,
            ),
        )

    @translate.register
    def _expr(
        self,
        expr: ir.Expr,
        **kwargs: Any,
    ) -> stalg.Expression:
        return self.translate(expr.op(), **kwargs)

    @translate.register
    def value(
        self,
        op: ops.Value,
        **kwargs: Any,
    ) -> stalg.Expression:
        # Check if scalar function is valid for input dtype(s) and insert casts as needed to
        # make sure inputs are correct.
        # TODO: add upcasting back
        op = self._check_and_upcast(op)
        # given the details of `op` -> function id
        return stalg.Expression(
            scalar_function=stalg.Expression.ScalarFunction(
                function_reference=self.compiler.function_id(op=op),
                output_type=self.translate(op.output_dtype),
                arguments=[
                    stalg.FunctionArgument(value=self.translate(arg, **kwargs))
                    for arg in op.args
                    if isinstance(arg, ops.Value)
                ],
            )
        )

    @staticmethod
    def _check_and_upcast(op: ops.Value) -> ops.Value:
        raise NotImplementedError

    @translate.register
    def _literal(
        self,
        op: ops.Literal,
        **kwargs: Any,
    ) -> stalg.Expression:
        dtype = op.output_dtype  # type: ignore
        value = op.value
        if value is None:
            return stalg.Expression(
                literal=stalg.Expression.Literal(null=self.translate(dtype, **kwargs))
            )
        return stalg.Expression(literal=self.translate_literal(dtype, op.value))

    @translate.register
    def alias_op(
        self,
        op: ops.Alias,
        **kwargs: Any,
    ) -> stalg.Expression:
        # For an alias, dispatch on the underlying argument
        return self.translate(op.arg, **kwargs)

    @translate.register
    def _reduction(
        self,
        op: ops.Reduction,
        **kwargs: Any,
    ) -> stalg.AggregateFunction:
        return stalg.AggregateFunction(
            function_reference=self.compiler.function_id(op=op),
            arguments=[stalg.FunctionArgument(value=self.translate(op.arg, **kwargs))],  # type: ignore
            sorts=[],  # TODO: ibis doesn't support this yet
            phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
            output_type=self.translate(op.output_dtype),
        )

    @translate.register
    def _count(
        self,
        op: ops.Count,
        **kwargs: Any,
    ) -> stalg.AggregateFunction:
        translated_args: list[stalg.FunctionArgument] = []
        arg = op.arg
        if not isinstance(arg, ops.TableNode):
            translated_args.append(
                stalg.FunctionArgument(value=self.translate(arg, **kwargs))
            )
        return stalg.AggregateFunction(
            function_reference=self.compiler.function_id(op=op),
            arguments=translated_args,
            sorts=[],  # TODO: ibis doesn't support this yet
            phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
            output_type=self.translate(op.output_dtype),
        )

    @translate.register(ops.SimpleCase)
    @translate.register(ops.SearchedCase)
    def _simple_searched_case(
        self,
        op: ops.SimpleCase | ops.SearchedCase,
        **kwargs: Any,
    ) -> stalg.Expression:
        # the field names for an `if_then` are `if` and `else` which means we need
        # to pass those args in as a dictionary to not run afoul of SyntaxErrors`
        _ifs = []
        for case, result in zip(op.cases, op.results):
            # TODO: this is a bit of a hack to handle SimpleCase vs. SearchedCase
            if_op = case if not hasattr(op, "base") else ops.Equals(op.base, case)  # type: ignore
            _if = {
                "if": self.translate(if_op, **kwargs),
                "then": self.translate(result, **kwargs),
            }
            _ifs.append(stalg.Expression.IfThen.IfClause(**_if))

        _else = {"else": self.translate(op.default, **kwargs)}

        return stalg.Expression(if_then=stalg.Expression.IfThen(ifs=_ifs, **_else))

    @translate.register
    def _where(
        self,
        op: ops.Where,
        **kwargs: Any,
    ) -> stalg.Expression:
        # the field names for an `if_then` are `if` and `else` which means we need
        # to pass those args in as a dictionary to not run afoul of SyntaxErrors`
        _if = {
            "if": self.translate(op.bool_expr, **kwargs),
            "then": self.translate(op.true_expr, **kwargs),
        }
        _else = {"else": self.translate(op.false_null_expr, **kwargs)}

        _ifs = [stalg.Expression.IfThen.IfClause(**_if)]

        return stalg.Expression(if_then=stalg.Expression.IfThen(ifs=_ifs, **_else))

    @translate.register
    def _contains(
        self,
        op: ops.Contains,
        **kwargs: Any,
    ) -> stalg.Expression:
        options = (
            op.options
            if isinstance(op.options, Iterable)
            else ibis.util.promote_list(op.options)
        )
        return stalg.Expression(
            singular_or_list=stalg.Expression.SingularOrList(
                value=self.translate(op.value, **kwargs),
                options=[self.translate(value, **kwargs) for value in options],
            )
        )

    @translate.register
    def _cast(
        self,
        op: ops.Cast,
        **kwargs: Any,
    ) -> stalg.Expression:
        return stalg.Expression(
            cast=stalg.Expression.Cast(
                type=self.translate(op.to),
                input=self.translate(op.arg, **kwargs),
                failure_behavior=stalg.Expression.Cast.FAILURE_BEHAVIOR_THROW_EXCEPTION,
            )
        )

    @translate.register
    def _log(
        self,
        op: ops.Log,
        **kwargs: Any,
    ) -> stalg.Expression:
        arg = stalg.FunctionArgument(value=self.translate(op.arg, **kwargs))
        base = stalg.FunctionArgument(
            value=self.translate(
                op.base if op.base is not None else ibis.literal(math.e),
                **kwargs,
            )
        )

        scalar_func = stalg.Expression.ScalarFunction(
            function_reference=self.compiler.function_id(op=op),
            output_type=self.translate(op.output_dtype),
            arguments=[arg, base],
        )
        return stalg.Expression(scalar_function=scalar_func)

    @translate.register
    def _floordivide(
        self,
        op: ops.FloorDivide,
        **kwargs: Any,
    ) -> stalg.Expression:
        left, right = op.left, op.right
        return self.translate((left / right).floor(), **kwargs)

    @translate.register
    def _clip(
        self,
        op: ops.Clip,
        **kwargs: Any,
    ) -> stalg.Expression:
        arg, lower, upper = op.arg, op.lower, op.upper

        if lower is not None and upper is not None:
            return self.translate(
                (arg >= lower).ifelse((arg <= upper).ifelse(arg, upper), lower),
                **kwargs,
            )
        elif lower is not None:
            return self.translate(
                (arg >= lower).ifelse(arg, lower),
                **kwargs,
            )
        elif upper is not None:
            return self.translate(
                (arg <= upper).ifelse(arg, upper),
                **kwargs,
            )
        raise AssertionError()

    @translate.register
    def _table_array_view(
        self,
        op: ops.TableArrayView,
        **kwargs: Any,
    ) -> stalg.Expression:
        return self.translate(op.table, **kwargs)

    @translate.register
    def _self_reference(
        self,
        op: ops.SelfReference,
        **kwargs: Any,
    ) -> stalg.Expression:
        return self.translate(op.table, **kwargs)

    @translate.register(ops.Floor)
    @translate.register(ops.Ceil)
    def _floor_ceil_cast(
        self,
        op: ops.Floor,
        **kwargs: Any,
    ) -> stalg.Expression:
        input = stalg.Expression(
            scalar_function=stalg.Expression.ScalarFunction(
                function_reference=self.compiler.function_id(op=op),
                output_type=self.translate(op.output_dtype),
                arguments=[
                    stalg.FunctionArgument(value=self.translate(arg, **kwargs))
                    for arg in op.func_args  # type: ignore
                    if isinstance(arg, (ir.Expr, ops.Value))
                ],
            )
        )
        return stalg.Expression(
            cast=stalg.Expression.Cast(
                type=self.translate(op.output_dtype),
                input=input,
                failure_behavior=stalg.Expression.Cast.FAILURE_BEHAVIOR_THROW_EXCEPTION,
            )
        )

    @translate.register
    def _extractdatefield(
        self,
        op: ops.ExtractDateField,
        **kwargs: Any,
    ) -> stalg.Expression:
        # e.g. "ExtractYear" -> "YEAR"
        span = type(op).__name__[len("Extract") :].upper()
        arguments = (
            stalg.FunctionArgument(value=self.translate(arg, **kwargs))
            for arg in op.args
            if isinstance(arg, (ir.Expr, ops.Value))
        )

        scalar_func = stalg.Expression.ScalarFunction(
            function_reference=self.compiler.function_id(op=op),
            output_type=self.translate(op.output_dtype),
        )
        scalar_func.arguments.add(enum=span)
        scalar_func.arguments.extend(arguments)
        return stalg.Expression(scalar_function=scalar_func)

    @translate.register
    def limit(
        self,
        op: ops.Limit,
        **kwargs: Any,
    ) -> stalg.Rel:
        return stalg.Rel(
            fetch=stalg.FetchRel(
                input=self.translate(op.table, **kwargs),
                offset=op.offset,
                count=op.n,
            )
        )

    @translate.register
    def set_op(
        self,
        op: ops.SetOp,
        **kwargs: Any,
    ) -> stalg.Rel:
        return stalg.Rel(
            set=stalg.SetRel(
                inputs=[
                    self.translate(op.left, **kwargs),
                    self.translate(op.right, **kwargs),
                ],
                op=translate_set_op_type(op),
            )
        )

    @translate.register
    def sort_key(
        self,
        op: ops.SortKey,
        **kwargs: Any,
    ) -> stalg.SortField:
        ordering = "ASC" if op.ascending else "DESC"
        return stalg.SortField(
            expr=self.translate(op.expr, **kwargs),
            direction=getattr(
                stalg.SortField.SortDirection,
                f"SORT_DIRECTION_{ordering}_NULLS_FIRST",
            ),
        )

    @translate.register(ops.TableColumn)
    def table_column(
        self,
        op: ops.TableColumn,
        child_rel_field_offsets: MutableMapping[ops.TableNode, int] | None = None,
        **kwargs: Any,
    ) -> stalg.Expression:
        schema = op.table.schema
        relative_offset = schema._name_locs[op.name]
        base_offset = (child_rel_field_offsets or {}).get(op.table, 0)
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

    def _filter_predicates(
        self,
        oppredicates: list[Any],
        table: ops.TableNode | ir.Table | None = None,
        relation: stalg.Rel | None = None,
        **kwargs: Any,
    ) -> stalg.Rel:
        relation = relation or self.translate(table)
        tuples = stalg.Rel(
            filter=stalg.FilterRel(
                input=relation,
                condition=self.translate(
                    functools.reduce(ops.And, oppredicates),  # type: ignore
                    **kwargs,
                ),
            )
        )

        return tuples

    @translate.register
    def _exists_subquery(
        self,
        op: ops.ExistsSubquery,
        **kwargs: Any,
    ) -> stalg.Expression:
        tuples = self._filter_predicates(
            op.predicates, table=op.foreign_table, **kwargs
        )

        return stalg.Expression(
            subquery=stalg.Expression.Subquery(
                set_predicate=stalg.Expression.Subquery.SetPredicate(
                    predicate_op=stalg.Expression.Subquery.SetPredicate.PREDICATE_OP_EXISTS,
                    tuples=tuples,
                )
            )
        )

    @translate.register
    def _not_exists_subquery(
        self,
        op: ops.NotExistsSubquery,
        **kwargs: Any,
    ) -> stalg.Expression:
        tuples = self._filter_predicates(
            op.predicates, table=op.foreign_table, **kwargs
        )

        return stalg.Expression(
            scalar_function=stalg.Expression.ScalarFunction(
                function_reference=self.compiler.function_id(op=ops.Not(op.to_expr())),  # type: ignore
                output_type=self.translate(op.output_dtype),
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

    @translate.register
    def _elementwise_udf(
        self,
        op: ops.ElementWiseVectorizedUDF,
        **kwargs: Any,
    ) -> stalg.Expression:
        if self.compiler.udf_uri is None:
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
        extension_uri = self.compiler.register_extension_uri(self.compiler.udf_uri)

        # Explicitly register extension function
        try:
            func_ext = self.compiler.function_extensions[udf_key]
        except KeyError:
            func_ext = self.compiler.function_extensions[
                udf_key
            ] = self.compiler.create_extension_function(extension_uri, op.func.__name__)

        return stalg.Expression(
            scalar_function=stalg.Expression.ScalarFunction(
                function_reference=func_ext.function_anchor,
                output_type=self.translate(op.return_type),
                arguments=[
                    stalg.FunctionArgument(value=self.translate(arg, **kwargs))
                    for arg in op.func_args
                    if isinstance(arg, ops.Value)
                ],
            )
        )

    @translate.register
    def unbound_table(
        self,
        op: ops.UnboundTable,
        **kwargs: Any,
    ) -> stalg.Rel:
        return stalg.Rel(
            read=stalg.ReadRel(
                # TODO: filter,
                # TODO: projection,
                common=stalg.RelCommon(direct=stalg.RelCommon.Direct()),
                base_schema=self.translate(op.schema),
                named_table=stalg.ReadRel.NamedTable(names=[op.name]),
            )
        )

    @translate.register
    def struct_field(
        self,
        op: ops.StructField,
        **kwargs: Any,
    ) -> stalg.Expression:
        child = self.translate(op.arg, **kwargs)
        field_name = op.field
        # TODO: store names/types inverse mapping on datatypes.Struct for O(1)
        # access to field index
        field_index = op.arg.output_dtype.names.index(field_name)

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

    def _get_child_relation_field_offsets(
        self,
        table: ops.TableNode,
    ) -> dict[ops.TableNode, int]:
        """Return the offset of each of table's fields.

        This function calculates the starting index of a relations fields, as if
        all relations were part of a single flat schema.

        """
        if isinstance(table, ops.Join):
            # Descend into the left and right tables to grab offsets from nested joins
            left_keys = self._get_child_relation_field_offsets(table.left)
            right_keys = self._get_child_relation_field_offsets(table.right)
            root_tables = [table.left, table.right]
            accum = [0, len(root_tables[0].schema)]
            return toolz.merge(left_keys, right_keys, dict(zip(root_tables, accum)))
        return {}

    def _mapping_counter(
        self,
        op: ops.Selection,
        rels: list[tuple[str, Any]],
        selections: Sequence[ir.Column],
    ) -> itertools.count:
        for relname, rel in rels:
            if relname == "aggregate" and rel.measures:
                mapping_counter = itertools.count(
                    len(rel.measures) + len(rel.groupings)
                )
                break
            elif output_mapping := rel.common.emit.output_mapping:
                mapping_counter = itertools.count(len(output_mapping))
                break
            elif not isinstance(op.table, ops.Join):
                # If child table is join, we cannot reliably call schema due to
                # potentially duplicate column names, so fallback to the orignal
                # logic.
                mapping_counter = itertools.count(len(op.table.schema))
                break
        else:
            source_tables = self._find_parent_tables(op)
            mapping_counter = itertools.count(
                sum(len(t.schema) for t in source_tables)  # type: ignore
            )

        return mapping_counter

    @translate.register(ops.Selection)
    def selection(
        self,
        op: ops.Selection,
        child_rel_field_offsets: MutableMapping[ops.TableNode, int] | None = None,
        **kwargs: Any,
    ) -> stalg.Rel:
        assert (
            not child_rel_field_offsets
        ), "non-empty child_rel_field_offsets passed in to selection translation rule"
        child_rel_field_offsets = self._get_child_relation_field_offsets(op.table)
        # source
        relation = self.translate(
            op.table,
            child_rel_field_offsets=child_rel_field_offsets,
            **kwargs,
        )
        # filter
        if op.predicates:
            relation = self._filter_predicates(
                op.predicates,
                relation=relation,
                child_rel_field_offsets=child_rel_field_offsets,
                **kwargs,
            )

        if selections := self._get_selections(op):
            rels = [
                (attr, getattr(relation, attr))
                for attr in (
                    "aggregate",
                    "cross",
                    "extension_leaf",
                    "extension_multi",
                    "extension_single",
                    "fetch",
                    "filter",
                    "join",
                    "project",
                    "read",
                    "set",
                    "sort",
                )
            ]
            mapping_counter = self._mapping_counter(op, rels, selections)

            relation = stalg.Rel(
                project=stalg.ProjectRel(
                    input=relation,
                    common=stalg.RelCommon(
                        emit=stalg.RelCommon.Emit(
                            output_mapping=[next(mapping_counter) for _ in selections]
                        )
                    ),
                    expressions=[
                        self.translate(
                            selection,
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
                        self.translate(
                            key,
                            child_rel_field_offsets=child_rel_field_offsets,
                            **kwargs,
                        )
                        for key in op.sort_keys
                    ],
                )
            )

        return relation

    @staticmethod
    def _get_selections(op: ops.Selection) -> Sequence[ir.Column]:
        raise NotImplementedError

    @staticmethod
    def _find_parent_tables(op: ops.Selection) -> set[ops.PhysicalTable]:
        raise NotImplementedError

    @translate.register
    def join(
        self,
        op: ops.Join,
        **kwargs: Any,
    ) -> stalg.Rel:
        child_rel_field_offsets = kwargs.pop("child_rel_field_offsets", None)
        child_rel_field_offsets = (
            child_rel_field_offsets or self._get_child_relation_field_offsets(op)
        )
        return stalg.Rel(
            join=stalg.JoinRel(
                left=self.translate(op.left, **kwargs),
                right=self.translate(op.right, **kwargs),
                expression=self.translate(
                    functools.reduce(ops.And, op.predicates),  # type: ignore
                    child_rel_field_offsets=child_rel_field_offsets,
                    **kwargs,
                ),
                type=_translate_join_type(op),
            )
        )

    @translate.register
    def aggregation(
        self,
        op: ops.Aggregation,
        **kwargs: Any,
    ) -> stalg.Rel:
        if op.having:
            raise NotImplementedError("`having` not yet implemented")

        table = op.table.to_expr()
        predicates = [pred.to_expr() for pred in op.predicates]
        # TODO: make this all ops
        table_expr = table.filter(predicates) if predicates else table
        input = self.translate(
            table_expr.op(),
            **kwargs,
        )

        # TODO: we handle sorts before aggregation here but we shouldn't be
        #
        # sorts should be compiled after after aggregation, because that is
        # semantically where they belong, but due to ibis storing sort keys in the
        # aggregate class we have to sort first, so ibis will use the correct base
        # table when decompiling
        if op.sort_keys:
            sorts = [self.translate(key, **kwargs) for key in op.sort_keys]
            input = stalg.Rel(sort=stalg.SortRel(input=input, sorts=sorts))

        aggregate = stalg.AggregateRel(
            input=input,
            groupings=[
                stalg.AggregateRel.Grouping(
                    grouping_expressions=[self.translate(by, **kwargs)]
                )
                for by in op.by
            ],
            measures=[
                stalg.AggregateRel.Measure(measure=self.translate(metric, **kwargs))
                for metric in op.metrics
            ],
        )

        return stalg.Rel(aggregate=aggregate)

    @functools.singledispatchmethod
    def translate_literal(
        self,
        dtype: dt.DataType,
        op: object,
    ) -> stalg.Expression.Literal:
        raise NotImplementedError(
            f"{dtype.__class__.__name__} literals are not yet implemented"
        )

    @translate_literal.register
    def _literal_boolean(
        self,
        dtype: dt.Boolean,
        value: bool,
    ) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(boolean=value)

    @translate_literal.register
    def _literal_int8(self, _: dt.Int8, value: int) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(i8=value)

    @translate_literal.register
    def _literal_int16(self, _: dt.Int16, value: int) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(i16=value)

    @translate_literal.register
    def _literal_int32(self, _: dt.Int32, value: int) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(i32=value)

    @translate_literal.register
    def _literal_int64(self, d_: dt.Int64, value: int) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(i64=value)

    @translate_literal.register
    def _literal_float32(self, _: dt.Float32, value: float) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(fp32=value)

    @translate_literal.register
    def _literal_float64(self, _: dt.Float64, value: float) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(fp64=value)

    @translate_literal.register
    def _literal_decimal(
        self, dtype: dt.Decimal, value: decimal.Decimal
    ) -> stalg.Expression.Literal:
        raise NotImplementedError

    @translate_literal.register
    def _literal_string(self, _: dt.String, value: str) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(string=value)

    @translate_literal.register
    def _literal_binary(self, _: dt.Binary, value: bytes) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(binary=value)

    @translate_literal.register
    def _literal_timestamp(
        self,
        dtype: dt.Timestamp,
        value: datetime.datetime,
    ) -> stalg.Expression.Literal:
        micros_since_epoch = int(value.timestamp() * 1e6)
        if dtype.timezone is not None:
            return stalg.Expression.Literal(timestamp_tz=micros_since_epoch)
        return stalg.Expression.Literal(timestamp=micros_since_epoch)

    @translate_literal.register
    def _literal_struct(
        self,
        dtype: dt.Struct,
        mapping: collections.OrderedDict,
    ) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(
            struct=stalg.Expression.Literal.Struct(
                fields=[
                    self.translate_literal(field_type, val)
                    for val, field_type in zip(mapping.values(), dtype.types)
                ]
            )
        )

    @translate_literal.register
    def _literal_map(
        self,
        dtype: dt.Map,
        mapping: collections.abc.MutableMapping,
    ) -> stalg.Expression.Literal:
        if not mapping:
            return stalg.Expression.Literal(empty_map=self.translate(dtype).map)
        return stalg.Expression.Literal(
            map=stalg.Expression.Literal.Map(
                key_values=[
                    stalg.Expression.Literal.Map.KeyValue(
                        key=self.translate_literal(dtype.key_type, key),
                        value=self.translate_literal(dtype.value_type, value),
                    )
                    for key, value in mapping.items()
                ],
            )
        )

    @translate_literal.register
    def _literal_array(
        self,
        dtype: dt.Array,
        sequence: Sequence[T],
    ) -> stalg.Expression.Literal:
        if not sequence:
            return stalg.Expression.Literal(empty_list=self.translate(dtype).list)
        return stalg.Expression.Literal(
            list=stalg.Expression.Literal.List(
                values=[
                    self.translate_literal(dtype.value_type, value)
                    for value in sequence
                ],
            )
        )

    @translate_literal.register(dt.UUID)
    def _literal_uuid(
        self, dtype: dt.UUID, value: str | uuid.UUID
    ) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(uuid=uuid.UUID(hex=str(value)).bytes)

    @translate_literal.register
    def _literal_time(
        self, time: dt.Time, value: datetime.time
    ) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(time=_time_to_micros(value))

    @translate_literal.register
    def _literal_date(
        self, date: dt.Date, value: datetime.date
    ) -> stalg.Expression.Literal:
        return stalg.Expression.Literal(date=_date_to_days(value))


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
