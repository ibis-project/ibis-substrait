"""The primary compiler interface."""

from __future__ import annotations

import base64
import functools
import itertools
from typing import Any, Hashable, Iterator

import cloudpickle
import google.protobuf.message as msg
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.types as ir
from ibis.expr.operations.vectorized import VectorizedUDF

from ..proto.substrait import algebra_pb2 as stalg
from ..proto.substrait import plan_pb2 as stp
from ..proto.substrait.extensions import extensions_pb2 as ste
from .mapping import IBIS_SUBSTRAIT_OP_MAPPING


def which_one_of(message: msg.Message, oneof_name: str) -> tuple[str, Any]:
    variant_name = message.WhichOneof(oneof_name)
    return variant_name, getattr(message, variant_name)


def _dict(**kwargs: Any) -> Any:
    return kwargs


@functools.singledispatch
def _function_name(*args: Any, **kwargs: Any) -> Any:
    raise NotImplementedError(*args)


@_function_name.register
def _default_fname(op: ops.ValueOp) -> str:
    return IBIS_SUBSTRAIT_OP_MAPPING[type(op).__name__]


@_function_name.register
def _udf_fname(op: VectorizedUDF) -> str:
    return op.func.__wrapped__.__name__


@functools.singledispatch
def _function_extension_kwds(*args: Any, **kwargs: Any) -> Any:
    raise NotImplementedError(*args)


@_function_extension_kwds.register
def _default_fext_kwds(op: ops.ValueOp, function_extension_kwds: dict) -> dict:
    return function_extension_kwds


@_function_extension_kwds.register
def _udf_fext_kwds(op: VectorizedUDF, function_extension_kwds: dict) -> dict:
    from .translate import translate

    function_extension_kwds.update(
        _dict(
            udf=(
                ste.SimpleExtensionDeclaration.ExtensionFunction.UserDefinedFunction(
                    code=base64.b64encode(
                        cloudpickle.dumps(op.func.__wrapped__)
                    ).decode("utf-8"),
                    summary=(
                        getattr(op, "func_summary", None)
                        or op.func.__wrapped__.__name__
                    ),
                    description=(
                        getattr(op, "func_desc", None) or op.func.__wrapped__.__doc__
                    ),
                    input_types=[translate(typ) for typ in op.input_type],
                    output_type=translate(op.return_type),
                )
            )
        )
    )
    return function_extension_kwds


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
        op_name = _function_name(op)
        try:
            function_extension = self.function_extensions[op_name]
        except KeyError:
            ste_decl = ste.SimpleExtensionDeclaration
            function_extension = self.function_extensions[
                op_name
            ] = ste_decl.ExtensionFunction(
                **_function_extension_kwds(
                    op,
                    _dict(
                        extension_uri_reference=self.extension_uri.extension_uri_anchor,
                        function_anchor=next(self.id_generator),
                        name=op_name,
                    ),
                )
            )
        return function_extension.function_anchor

    def compile(self, expr: ir.TableExpr) -> stp.Plan:
        """Construct a Substrait plan from an ibis table expression."""
        from .translate import translate

        expr_schema = expr.schema()
        rel = stp.PlanRel(
            root=stalg.RelRoot(
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
    >>> list(_get_fields(array_type))  # doctest: +SKIP
    [(None, int64)]
    >>> map_type = dt.parse_type("map<string, string>")
    >>> list(_get_fields(map_type))
    [(None, String(nullable=True)), (None, String(nullable=True))]
    >>> struct_type = dt.parse_type("struct<a: int64, b: map<int64, float64>>")
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
