"""The primary compiler interface."""

from __future__ import annotations

import itertools
from typing import Any, Hashable, Iterator

import google.protobuf.message as msg
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.types as ir

from ibis_substrait.compiler.mapping import (
    IBIS_SUBSTRAIT_OP_MAPPING,
    IBIS_SUBSTRAIT_TYPE_MAPPING,
    _extension_mapping,
)
from ibis_substrait.proto.substrait.ibis import algebra_pb2 as stalg
from ibis_substrait.proto.substrait.ibis import plan_pb2 as stp
from ibis_substrait.proto.substrait.ibis.extensions import extensions_pb2 as ste


def which_one_of(message: msg.Message, oneof_name: str) -> tuple[str, Any]:
    variant_name = message.WhichOneof(oneof_name)
    return variant_name, getattr(message, variant_name)


class SubstraitCompiler:
    def __init__(self, udf_uri: str | None = None) -> None:
        """Initialize the compiler.

        Parameters
        ----------
        udf_uri
            The extension URI to use for looking up registered UDFs, if any.
            This is highly backend dependent.
        """
        self.extension_uris: dict[str, ste.SimpleExtensionURI] = {}
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
        # start at 1 because 0 is the default value for the type
        self.id_generator = itertools.count(1)

        self.udf_uri = udf_uri

    def function_id(
        self,
        *,
        expr: ir.ValueExpr | None = None,
        op: ops.Value | None = None,
    ) -> int:
        """Create a function mapping for a given expression.

        Parameters
        ----------
        expr
            An ibis expression that produces a value.
        op
            Passthrough op to directly specify desired substrait scalar function

        Returns
        -------
        ste.ExtensionsFunctionId
            This is a unique identifier for a given operation type, *argument
            types N-tuple.
        """
        if op is None:
            op = expr.op() if expr is not None else None
        op_type = type(op)
        op_name = IBIS_SUBSTRAIT_OP_MAPPING[op_type.__name__]

        try:
            function_extension = self.function_extensions[op_name]
        except KeyError:
            function_extension = self.function_extensions[
                op_name
            ] = self.extension_lookup(op_name, op)
        return function_extension.function_anchor

    def extension_lookup(
        self,
        op_name: str,
        op: ops.Node,
    ) -> ste.SimpleExtensionDeclaration.ExtensionFunction:
        if not _extension_mapping.get(op_name, False):
            raise ValueError(
                f"No available extension defined for function name {op_name}"
            )

        anykey = ("any",) * len([arg for arg in op.args if arg is not None])

        # First check if `any` is an option
        # This function will take arguments of any type
        # although we still want to check if the number of args is correct
        function_extension = _extension_mapping[op_name].get(anykey)

        # Then try to look up extension based on input datatypes
        # Each substrait function defines the types of the inputs and at this
        # stage we should have performed the appropriate casts to ensure that
        # argument types match.
        if function_extension is None:
            sigkey = tuple(
                [
                    IBIS_SUBSTRAIT_TYPE_MAPPING[arg.op().output_dtype.name]
                    for arg in op.args
                    if arg is not None
                ]
            )
            function_extension = _extension_mapping[op_name].get(sigkey)

        # Then check if extension is variadic
        # If we're here, then it's possible that we're trying to lookup a valid
        # signature that looks like ("boolean", "boolean") but we aren't having any
        # luck because the function is variadic.  In this case, the variadic argument
        # type is only repeated once, so we try to perform a lookup that way, then
        # assert, if we find anything, that the function is, indeed, variadic.
        if function_extension is None:
            function_extension = _extension_mapping[op_name].get((sigkey[0],))
            if function_extension is not None:
                assert function_extension.variadic

        # If it's still None then we're borked.
        if function_extension is None:
            raise ValueError(
                f"No matching extension type found for function {op_name} with input types {sigkey}"
            )

        extension_uri = self.register_extension_uri(function_extension.uri)

        extension_function = self.create_extension_function(extension_uri, op_name)

        return extension_function

    def create_extension_function(
        self, extension_uri: ste.SimpleExtensionURI, scalar_func: str
    ) -> ste.SimpleExtensionDeclaration.ExtensionFunction:
        """Define an extension function with reference to the definition URI.

        Parameters
        ----------
        extension_uri
            A registered SimpleExtensionURI that points to the extension
            function definition site
        scalar_func
            The name of the scalar function

        Returns
        -------
        ste.SimpleExtensionDeclaration.ExtensionFunction
        """
        return ste.SimpleExtensionDeclaration.ExtensionFunction(
            extension_uri_reference=extension_uri.extension_uri_anchor,
            function_anchor=next(self.id_generator),
            name=scalar_func,
        )

    def register_extension_uri(self, uri: str) -> ste.SimpleExtensionURI:
        """Create or retrieve the extension URI substrait entry for the given uri.

        Parameters
        ----------
        uri
            The URI pointing to the extension function definition location

        Returns
        -------
        ste.SimpleExtensionURI
        """
        try:
            extension_uri = self.extension_uris[uri]
        except KeyError:
            extension_uri = self.extension_uris[uri] = ste.SimpleExtensionURI(
                # by convention, extension URIs start at 1
                extension_uri_anchor=len(self.extension_uris) + 1,
                uri=uri,
            )

        return extension_uri

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
            extension_uris=list(self.extension_uris.values()),
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
