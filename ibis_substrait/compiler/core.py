"""The primary compiler interface."""

from __future__ import annotations

import itertools
from typing import Any, Hashable, Iterator

import google.protobuf.message as msg
import ibis.expr.datatypes as dt
import ibis.expr.types as ir
import inflection

from ..proto.substrait import plan_pb2 as stp
from ..proto.substrait import relations_pb2 as strel
from ..proto.substrait.extensions import extensions_pb2 as ste


def which_one_of(message: msg.Message, oneof_name: str) -> tuple[str, Any]:
    variant_name = message.WhichOneof(oneof_name)
    return variant_name, getattr(message, variant_name)


class SubstraitCompiler:
    def __init__(self) -> None:
        """Initialize the compiler."""
        # start at id 1 because 0 is the default proto value for the type
        self.extension_uri = ste.SimpleExtensionURI(extension_uri_anchor=1)
        self.function_extensions: dict[
            tuple[Hashable, ...],
            ste.SimpleExtensionDeclaration.ExtensionFunction,
        ] = {}
        self.type_extensions: dict[
            int,
            ste.SimpleExtensionDeclaration.ExtensionType,
        ] = {}
        self.type_variations: dict[
            int,
            ste.SimpleExtensionDeclaration.ExtensionTypeVariation,
        ] = {}
        # similarly, start at 1 because 0 is the default value for the type
        self.id_generator = itertools.count(1)

    def function_id(self, expr: ir.ValueExpr) -> int:
        """Create a function mapping for a given expression.

        Parameters
        ----------
        expr
            An ibis expression that produces a value.

        Returns
        -------
        ste.ExtensionsFunctionId
            This is a unique identifier for a given operation type, *argument
            types N-tuple.
        """
        op = expr.op()
        op_type = type(op)
        type_args = tuple(
            arg.type() for arg in op.args if isinstance(arg, ir.ValueExpr)
        )
        key = op_type, *type_args
        try:
            function_extension = self.function_extensions[key]
        except KeyError:
            function_extension = self.function_extensions[
                key
            ] = ste.SimpleExtensionDeclaration.ExtensionFunction(
                extension_uri_reference=self.extension_uri.extension_uri_anchor,
                function_anchor=next(self.id_generator),
                name=inflection.underscore(op_type.__name__),
            )
        return function_extension.function_anchor

    def compile(self, expr: ir.TableExpr) -> stp.Plan:
        """Construct a Substrait plan from an ibis table expression."""
        from .translate import translate

        expr_schema = expr.materialize().schema()
        rel = stp.PlanRel(
            root=strel.RelRoot(
                input=translate(expr.op(), expr, self),
                names=translate(expr_schema).names,
            )
        )
        return stp.Plan(
            extension_uris=[self.extension_uri],
            extensions=list(
                itertools.chain(
                    (
                        ste.SimpleExtensionDeclaration(
                            extension_function=extension_function
                        )
                        for extension_function in self.function_extensions.values()
                    ),
                    (
                        ste.SimpleExtensionDeclaration(extension_type=extension_type)
                        for extension_type in self.type_extensions.values()
                    ),
                    (
                        ste.SimpleExtensionDeclaration(
                            extension_type_variation=extension_type_variation
                        )
                        for extension_type_variation in self.type_variations.values()
                    ),
                )
            ),
            relations=[rel],
        )


class SubstraitDecompiler:
    def __init__(self, plan: stp.Plan) -> None:
        """Initialize the decompiler with a :class:`Plan`."""
        self.function_extensions = {
            ext.extension_function.function_anchor: ext.extension_function
            for ext in plan.extensions
            if ext.WhichOneof("mapping_type") == "extension_function"
        }
        self.type_extensions = {
            ext.extension_type.type_anchor: ext.extension_type
            for ext in plan.extensions
            if ext.WhichOneof("mapping_type") == "extension_type"
        }
        self.type_variations = {
            ext.extension_type_variation.type_variation_anchor: ext.extension_type_variation  # noqa: E501
            for ext in plan.extensions
            if ext.WhichOneof("mapping_type") == "extension_type_variation"
        }
        self.extension_uris = plan.extension_uris


def _get_fields(dtype: dt.DataType) -> Iterator[tuple[str | None, dt.DataType]]:
    """Extract fields from `dtype`.

    Examples
    --------
    >>> import ibis.expr.datatypes as dt
    >>> array_type = dt.parse_type("array<int64>")
    >>> list(_get_fields(array_type))
    [(None, int64)]
    >>> map_type = dt.parse_type("map<string, string>")
    >>> list(_get_fields(map_type))
    [(None, String(nullable=True)), (None, String(nullable=True))]
    >>> struct_type = dt.parse_type("struct<a: int64, b: map<int64, float64>>")
    >>> list(_get_fields(struct_type))
    [('b', Map(key_type=int64, value_type=float64, nullable=True)), ('a', int64)]
    """
    if isinstance(dtype, dt.Array):
        yield None, dtype.value_type
    elif isinstance(dtype, dt.Map):
        yield None, dtype.value_type
        yield None, dtype.key_type
    elif isinstance(dtype, dt.Struct):
        yield from reversed(list(dtype.pairs.items()))
