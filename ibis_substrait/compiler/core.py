"""The primary compiler interface."""

from __future__ import annotations

import itertools
from collections.abc import Hashable, Iterator
from typing import TYPE_CHECKING, Any

import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.types as ir
from packaging.version import parse as vparse
from substrait.gen.proto import algebra_pb2 as stalg
from substrait.gen.proto import plan_pb2 as stp
from substrait.gen.proto.extensions import extensions_pb2 as ste

from ibis_substrait import __substrait_hash__, __substrait_version__
from ibis_substrait.compiler.mapping import (
    IBIS_SUBSTRAIT_OP_MAPPING,
    IBIS_SUBSTRAIT_TYPE_MAPPING,
    _extension_mapping,
)

if TYPE_CHECKING:
    import google.protobuf.message as msg


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
        op: ops.Value,
    ) -> int:
        """Create a function mapping for a given expression.

        Parameters
        ----------
        op
            Ibis operation to use to lookup desired substrait scalar function

        Returns
        -------
        ste.ExtensionsFunctionId
            This is a unique identifier for a given operation type, *argument
            types N-tuple.

        """

        op_name = IBIS_SUBSTRAIT_OP_MAPPING[type(op).__name__]
        sig_key = self.get_signature(op)

        extension_signature = f"{op_name}:{'_'.join(sig_key)}"

        try:
            function_extension = self.function_extensions[extension_signature]
        except KeyError:
            function_extension = self.function_extensions[extension_signature] = (
                self.create_extension(op_name, sig_key)
            )
        return function_extension.function_anchor

    def get_signature(self, op: ops.Node) -> tuple[str, ...]:
        """Validate and upcast (if necessary) scalar function extension signature."""

        op_name = IBIS_SUBSTRAIT_OP_MAPPING[type(op).__name__]

        if not _extension_mapping.get(op_name, False):
            raise ValueError(
                f"No available extension defined for function name {op_name}"
            )

        anykey = ("any",) * len([arg for arg in op.args if arg is not None])
        sigkey = anykey

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
                    IBIS_SUBSTRAIT_TYPE_MAPPING[arg.dtype.name]  # type: ignore
                    for arg in op.args
                    if arg is not None and isinstance(arg, ops.Node)
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
                # Function signature for a variadic should contain the type of
                # the argument(s) at _least_ once but ideally should contain
                # types == the minimum number of variadic args allowed (but keep
                # it nonzero)
                arg_count_min = max(function_extension.variadic.get("min", 0), 1)
                sigkey = (sigkey[0],) * arg_count_min

        # If it's still None then we're borked.
        if function_extension is None:
            raise ValueError(
                f"No matching extension type found for function {op_name} with input types {sigkey}"
            )

        return sigkey

    def create_extension(
        self,
        op_name: str,
        sigkey: tuple[str, ...],
    ) -> ste.SimpleExtensionDeclaration.ExtensionFunction:
        """Register extension uri and create extension function."""

        function_extension = _extension_mapping[op_name][sigkey]
        extension_uri = self.register_extension_uri(function_extension.uri)

        extension_function = self.create_extension_function(
            extension_uri, f"{op_name}:{'_'.join(sigkey)}"
        )

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

    def compile(self, expr: ir.Table, **kwargs: Any) -> stp.Plan:
        """Construct a Substrait plan from an ibis table expression."""
        from .translate import translate

        expr_schema = expr.schema()
        rel = stp.PlanRel(
            root=stalg.RelRoot(
                input=translate(expr.op(), compiler=self, **kwargs),
                names=translate(expr_schema).names,
            )
        )
        ver = vparse(__substrait_version__)
        return stp.Plan(
            version=stp.Version(
                major_number=ver.major,
                minor_number=ver.minor,
                patch_number=ver.micro,
                git_hash=__substrait_hash__ if ver.is_devrelease else "",
                producer="ibis-substrait",
            ),
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
        # Ibis 3
        pairs = getattr(dtype, "pairs", None)
        if pairs is None:
            # Ibis 4 and 5
            pairs = getattr(dtype, "fields", None)

        if pairs is None:
            raise AttributeError
        yield from reversed(list(pairs.items()))
