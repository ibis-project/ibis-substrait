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
from ibis_substrait.compiler.function_registry import FunctionRegistry
from ibis_substrait.compiler.mapping import (
    IBIS_SUBSTRAIT_OP_MAPPING,
    ibis_type_to_substrait,
)

if TYPE_CHECKING:
    import google.protobuf.message as msg


def which_one_of(message: msg.Message, oneof_name: str) -> tuple[str, Any]:
    variant_name = message.WhichOneof(oneof_name)
    return variant_name, getattr(message, variant_name)


default_registry = FunctionRegistry()


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

        self.function_registry = default_registry

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

        substrait_ops = IBIS_SUBSTRAIT_OP_MAPPING[type(op).__name__]

        input_signature = tuple(
            [
                ibis_type_to_substrait(arg.dtype)  # type: ignore
                for arg in op.args
                if arg is not None and isinstance(arg, ops.Value)
            ]
        )

        for substrait_op in substrait_ops:
            func_tuple = self.function_registry.lookup_function(
                uri=substrait_op[0],
                function_name=substrait_op[1],
                signature=input_signature,
            )
            if func_tuple:
                (func, rtn) = func_tuple
                break

        if func_tuple is None:
            raise Exception(
                f"Could't find a function that satisfies the requirements {type(op).__name__} with {input_signature}"
            )

        extension_signature = str(func)

        try:
            function_extension = self.function_extensions[extension_signature]
        except KeyError:
            extension_uri = self.register_extension_uri(func.uri)

            function_extension = self.function_extensions[extension_signature] = (
                self.create_extension_function(extension_uri, extension_signature)
            )
        return function_extension.function_anchor

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
