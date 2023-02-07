"""The primary compiler interface."""

from __future__ import annotations

import itertools
from typing import Any, Hashable, Iterator

import google.protobuf.message as msg
import ibis.expr.datatypes as dt
import ibis.expr.types as ir

from ibis_substrait.proto.substrait.ibis import algebra_pb2 as stalg
from ibis_substrait.proto.substrait.ibis import plan_pb2 as stp
from ibis_substrait.proto.substrait.ibis.extensions import extensions_pb2 as ste

from .mapping import IBIS_SUBSTRAIT_OP_MAPPING


def which_one_of(message: msg.Message, oneof_name: str) -> tuple[str, Any]:
    variant_name = message.WhichOneof(oneof_name)
    return variant_name, getattr(message, variant_name)


class SubstraitCompiler:
    def __init__(self, uri: str | None = None) -> None:
        """Initialize the compiler.

        Parameters
        ----------
        uri
            The extension URI to use, if any.
        """
        # start at id 1 because 0 is the default proto value for the type
        self.extension_uri = (
            ste.SimpleExtensionURI(extension_uri_anchor=1)
            if uri is None
            else ste.SimpleExtensionURI(extension_uri_anchor=1, uri=uri)
        )
        self.function_extensions: dict[
            str | tuple[Hashable, ...],
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

    def function_id(
        self, *, expr: ir.ValueExpr | None = None, op_name: str | None = None
    ) -> int:
        """Create a function mapping for a given expression.

        Parameters
        ----------
        expr
            An ibis expression that produces a value.
        op_name
            Passthrough argument to directly specify desired substrait scalar function

        Returns
        -------
        ste.ExtensionsFunctionId
            This is a unique identifier for a given operation type, *argument
            types N-tuple.
        """
        if op_name is None:
            op = expr.op() if expr is not None else None
            op_type = type(op)
            op_name = IBIS_SUBSTRAIT_OP_MAPPING[op_type.__name__]

        try:
            function_extension = self.function_extensions[op_name]
        except KeyError:
            function_extension = self.function_extensions[
                op_name
            ] = ste.SimpleExtensionDeclaration.ExtensionFunction(
                extension_uri_reference=self.extension_uri.extension_uri_anchor,
                function_anchor=next(self.id_generator),
                name=op_name,
            )
        return function_extension.function_anchor

    def compile(self, expr: ir.TableExpr, **kwargs: Any) -> stp.Plan:
        """Construct a Substrait plan from an ibis table expression."""
        from .translate import translate

        expr_schema = expr.schema()
        rel = stp.PlanRel(
            root=stalg.RelRoot(
                input=translate(expr.op(), expr=expr, compiler=self, **kwargs),
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
            ext.extension_type_variation.type_variation_anchor: ext.extension_type_variation
            for ext in plan.extensions
            if ext.WhichOneof("mapping_type") == "extension_type_variation"
        }
        self.extension_uris = plan.extension_uris


def _get_fields(dtype: dt.DataType) -> Iterator[tuple[str | None, dt.DataType]]:
    """Extract fields from `dtype`.

    Examples
    --------
    >>> import ibis.expr.datatypes as dt
    >>> array_type = dt.parse("array<int64>")
    >>> list(_get_fields(array_type))  # doctest: +SKIP
    [(None, int64)]
    >>> map_type = dt.parse("map<string, string>")
    >>> list(_get_fields(map_type))
    [(None, String(nullable=True)), (None, String(nullable=True))]
    >>> struct_type = dt.parse("struct<a: int64, b: map<int64, float64>>")
    >>> list(_get_fields(struct_type))  # doctest: +SKIP
    [('b', Map(key_type=int64, value_type=float64, nullable=True)), ('a', int64)]
    """
    if isinstance(dtype, dt.Array):
        yield None, dtype.value_type
    elif isinstance(dtype, dt.Map):
        yield None, dtype.value_type
        yield None, dtype.key_type
    elif isinstance(dtype, dt.Struct):
        yield from reversed(list(dtype.pairs.items()))
