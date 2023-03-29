# mypy: ignore-errors

from __future__ import annotations

import functools
import itertools
import operator
from typing import TYPE_CHECKING, Any, Mapping, MutableMapping, Sequence, Union

import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.types as ir
import toolz
from ibis.util import to_op_dag

from ibis_substrait.compiler.mapping import (
    IBIS_SUBSTRAIT_OP_MAPPING,
    _extension_mapping,
)
from ibis_substrait.compiler.translator.base import IbisTranslator, _translate_join_type
from ibis_substrait.compiler.translator.window import _translate_window_bounds
from ibis_substrait.proto.substrait.ibis import algebra_pb2 as stalg

if TYPE_CHECKING:
    from ibis_substrait.compiler.core import SubstraitCompiler

try:
    from typing import TypeAlias
except ImportError:
    # Python <=3.9
    from typing_extensions import TypeAlias


class Ibis3Translator(IbisTranslator):
    def __init__(self, compiler: SubstraitCompiler) -> None:
        super().__init__(compiler)
        _inherited_registry = IbisTranslator.__dict__[
            "translate"
        ].dispatcher.registry.copy()
        _registry = Ibis3Translator.__dict__["translate"].dispatcher.registry.copy()
        registry_keys = set(_registry.keys())
        for cls, func in _inherited_registry.items():
            if cls not in registry_keys:
                self.translate.register(cls, func)

    @functools.singledispatchmethod
    def translate(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @translate.register(ops.Value)
    def value_op(
        self,
        op: ops.Value,
        **kwargs: Any,
    ) -> stalg.Expression:
        # Check if scalar function is valid for input dtype(s) and insert casts
        # as needed to make sure inputs are correct.
        op = self._check_and_upcast(op)
        # given the details of `op` -> function id
        return stalg.Expression(
            scalar_function=stalg.Expression.ScalarFunction(
                function_reference=self.compiler.function_id(op=op),
                output_type=self.translate(op.output_dtype),
                arguments=[
                    stalg.FunctionArgument(value=self.translate(arg, **kwargs))
                    for arg in op.args
                    if isinstance(arg, ir.Expr)
                ],
            )
        )

    @translate.register
    def _count(
        self,
        op: ops.Count,
        **kwargs: Any,
    ) -> stalg.AggregateFunction:
        translated_args: list[stalg.FunctionArgument] = []
        arg = op.arg.op().to_expr()
        if not isinstance(arg, ir.TableExpr):
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

    @translate.register
    def _exists_subquery(
        self,
        op: ops.ExistsSubquery,
        **kwargs: Any,
    ) -> stalg.Expression:
        predicates = [pred.op().to_expr() for pred in op.predicates]
        tuples = stalg.Rel(
            filter=stalg.FilterRel(
                input=self.translate(op.foreign_table),
                condition=self.translate(
                    functools.reduce(operator.and_, predicates),
                    **kwargs,
                ),
            )
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
        predicates = [pred.op().to_expr() for pred in op.predicates]
        tuples = stalg.Rel(
            filter=stalg.FilterRel(
                input=self.translate(op.foreign_table),
                condition=self.translate(
                    functools.reduce(operator.and_, predicates),
                    **kwargs,
                ),
            )
        )

        return stalg.Expression(
            scalar_function=stalg.Expression.ScalarFunction(
                function_reference=self.compiler.function_id(op=ops.Not(op.to_expr())),
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
    def selection(
        self,
        op: ops.Selection,
        *,
        child_rel_field_offsets: Mapping[ops.TableNode, int] | None = None,
        **kwargs: Any,
    ) -> stalg.Rel:
        assert (
            not child_rel_field_offsets
        ), "non-empty child_rel_field_offsets passed in to selection translation rule"
        # Explicitly v3
        child_rel_field_offsets = self._get_child_relation_field_offsets(op.table)
        # source
        relation = self.translate(
            op.table,
            child_rel_field_offsets=child_rel_field_offsets,
            **kwargs,
        )
        # filter
        if op.predicates:
            predicates = [pred.op().to_expr() for pred in op.predicates]
            relation = stalg.Rel(
                filter=stalg.FilterRel(
                    input=relation,
                    condition=self.translate(
                        # Explicitly v3
                        functools.reduce(operator.and_, predicates).op(),
                        child_rel_field_offsets=child_rel_field_offsets,
                        **kwargs,
                    ),
                )
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
            for relname, rel in rels:
                if relname == "aggregate" and rel.measures:
                    mapping_counter = itertools.count(
                        len(rel.measures) + len(rel.groupings)
                    )
                    break
                elif output_mapping := rel.common.emit.output_mapping:
                    mapping_counter = itertools.count(len(output_mapping))
                    break
                elif not isinstance(op.table.op(), ops.Join):
                    # If child table is join, we cannot reliably call schema due to
                    # potentially duplicate column names, so fallback to the orignal
                    # logic.
                    mapping_counter = itertools.count(len(op.table.op().schema))
                    break
            else:
                source_tables = self._find_parent_tables(op)
                mapping_counter = itertools.count(
                    sum(len(t.schema) for t in source_tables)
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

    def _get_child_relation_field_offsets(
        self, table: ir.TableExpr
    ) -> dict[ops.TableNode, int]:
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
            left_keys = self._get_child_relation_field_offsets(table_op.left)
            right_keys = self._get_child_relation_field_offsets(table_op.right)
            root_tables = [table_op.left.op(), table_op.right.op()]
            accum = [0, len(root_tables[0].schema)]
            return toolz.merge(left_keys, right_keys, dict(zip(root_tables, accum)))
        return {}

    @staticmethod
    def _get_selections(op: ops.Selection) -> Sequence[ir.Column]:
        # projection / emit
        selections = [
            col
            for sel in op.selections
            for col in (
                sel.get_columns(sel.columns) if isinstance(sel, ir.TableExpr) else [sel]
            )
        ]

        return selections

    @staticmethod
    def _find_parent_tables(op: ops.Selection) -> set[ir.Table]:
        # TODO: settle on a better source table definition than "PhysicalTable with
        # a schema"
        source_tables = {
            t
            for t in to_op_dag(op.to_expr()).keys()
            if isinstance(t, ops.PhysicalTable) and hasattr(t, "schema")
        }

        return source_tables

    @translate.register
    def aggregation(
        self,
        op: ops.Aggregation,
        **kwargs: Any,
    ) -> stalg.Rel:
        if op.having:
            raise NotImplementedError("`having` not yet implemented")

        table = op.table.op().to_expr()
        predicates = [pred.op().to_expr() for pred in op.predicates]
        input = self.translate(
            table.filter(predicates) if predicates else table,
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

    @translate.register
    def join(
        self,
        op: ops.Join,
        **kwargs: Any,
    ) -> stalg.Rel:
        child_rel_field_offsets = kwargs.pop("child_rel_field_offsets", None)
        child_rel_field_offsets = (
            child_rel_field_offsets
            or self._get_child_relation_field_offsets(op.to_expr())
        )
        predicates = [pred.op().to_expr() for pred in op.predicates]
        return stalg.Rel(
            join=stalg.JoinRel(
                left=self.translate(op.left, **kwargs),
                right=self.translate(op.right, **kwargs),
                expression=self.translate(
                    functools.reduce(operator.and_, predicates),
                    child_rel_field_offsets=child_rel_field_offsets,
                    **kwargs,
                ),
                type=_translate_join_type(op),
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
        field_index = op.arg.op().output_dtype.names.index(field_name)

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

    @translate.register
    def table_column(
        self,
        op: ops.TableColumn,
        child_rel_field_offsets: MutableMapping[ops.TableNode, int] | None = None,
        **kwargs: Any,
    ) -> stalg.Expression:
        schema = op.table.op().schema
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

    @translate.register
    def window_op(
        self,
        op: ops.WindowOp,
        **kwargs: Any,
    ) -> stalg.Expression:
        window_gb = op.window._group_by
        window_ob = op.window._order_by
        start = op.window.preceding
        end = op.window.following
        func = {"expr": op.expr}
        func_args = op.expr.op().args

        lower_bound, upper_bound = _translate_window_bounds(start, end)

        return stalg.Expression(
            window_function=stalg.Expression.WindowFunction(
                function_reference=self.compiler.function_id(**func),
                partitions=[self.translate(gb, **kwargs) for gb in window_gb],
                sorts=[self.translate(ob, **kwargs) for ob in window_ob],
                output_type=self.translate(op.output_dtype),
                phase=stalg.AggregationPhase.AGGREGATION_PHASE_INITIAL_TO_RESULT,
                arguments=[
                    stalg.FunctionArgument(value=self.translate(arg, **kwargs))
                    for arg in func_args
                    if isinstance(arg, ir.Expr)
                ],
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )
        )

    @staticmethod
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
    left, right = op.left.op().output_dtype, op.right.op().output_dtype

    if left == right:
        return op
    elif dt.castable(left, right, upcast=True):
        return type(op)(op.left.cast(right), op.right)  # type: ignore
    elif dt.castable(right, left, upcast=True):
        return type(op)(op.left, op.right.cast(left))  # type: ignore
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
        newop.cast(dt.Int32()) if isinstance(newop.type(), dt.SignedInteger) else newop
        for newop in op.args
    ]

    return type(op)(*casted_args)
