from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Sequence, Union

import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.types as ir

from ibis_substrait.compiler.mapping import (
    IBIS_SUBSTRAIT_OP_MAPPING,
    _extension_mapping,
)
from ibis_substrait.compiler.translator.base import IbisTranslator
from ibis_substrait.compiler.translator.window import _translate_window_bounds
from ibis_substrait.proto.substrait.ibis import algebra_pb2 as stalg

if TYPE_CHECKING:
    from ibis_substrait.compiler.core import SubstraitCompiler


try:
    from typing import TypeAlias
except ImportError:
    # Python <=3.9
    from typing_extensions import TypeAlias


class Ibis4Translator(IbisTranslator):
    def __init__(self, compiler: SubstraitCompiler) -> None:
        super().__init__(compiler)
        _inherited_registry = IbisTranslator.__dict__[
            "translate"
        ].dispatcher.registry.copy()
        _registry = Ibis4Translator.__dict__["translate"].dispatcher.registry.copy()
        registry_keys = set(_registry.keys())
        for cls, func in _inherited_registry.items():
            if cls not in registry_keys:
                self.translate.register(cls, func)  # type: ignore

    @functools.singledispatchmethod
    def translate(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @translate.register
    def window(
        self,
        op: ops.Window,  # type: ignore
        **kwargs: Any,
    ) -> stalg.Expression:
        window_gb = op.window._group_by
        window_ob = op.window._order_by
        start = op.window.preceding
        end = op.window.following
        func = {"expr": op.expr}
        func_args = op.expr.args

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
                    if isinstance(arg, ops.Value)
                ],
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )
        )

    @translate.register(ops.CountStar)
    def _countstar(
        self,
        op: ops.CountStar,
        **kwargs: Any,
    ) -> stalg.AggregateFunction:
        return self._count(op, **kwargs)

    @staticmethod
    def _get_selections(op: ops.Selection) -> Sequence[ir.Column]:
        # projection / emit
        selections = [
            col
            for sel in (x.to_expr() for x in op.selections)  # map ops to exprs
            for col in (
                map(sel.__getitem__, sel.columns)
                if isinstance(sel, ir.Table)
                else [sel]
            )
        ]

        return selections

    @staticmethod
    def _find_parent_tables(op: ops.Selection) -> set[ops.PhysicalTable]:
        # TODO: settle on a better source table definition than "PhysicalTable with
        # a schema"
        source_tables = {
            t
            for t in toposort(op).keys()
            if isinstance(t, ops.PhysicalTable) and hasattr(t, "schema")
        }

        return source_tables

    @staticmethod
    def _check_and_upcast(op: ops.Value) -> ops.Value:
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
    left, right = op.left.output_dtype, op.right.output_dtype

    if left == right:
        return op
    elif dt.castable(left, right, upcast=True):
        return type(op)(ops.Cast(op.left, to=right), op.right)  # type: ignore
    elif dt.castable(right, left, upcast=True):
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
        ops.Cast(newop, to=dt.Int32())  # type: ignore
        if isinstance(newop.output_dtype, dt.SignedInteger)
        else newop
        for newop in op.args
    ]
    return type(op)(*casted_args)
