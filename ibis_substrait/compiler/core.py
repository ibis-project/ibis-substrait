"""The primary compiler interface."""

from __future__ import annotations

import itertools
from functools import singledispatch
from typing import Any, Hashable, Iterator

import google.protobuf.message as msg
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.types as ir

from ..proto.substrait.ibis import algebra_pb2 as stalg
from ..proto.substrait.ibis import plan_pb2 as stp
from ..proto.substrait.ibis.extensions import extensions_pb2 as ste
from .mapping import FUNCTION_SIGNATURES, IBIS_SUBSTRAIT_OP_MAPPING


def which_one_of(message: msg.Message, oneof_name: str) -> tuple[str, Any]:
    variant_name = message.WhichOneof(oneof_name)
    return variant_name, getattr(message, variant_name)


@singledispatch
def op_signature(op: ops.Any) -> Any:
    raise NotImplementedError


@op_signature.register
def _binary(op: ops.Binary) -> tuple[str, str, str]:
    from .translate import translate

    left_type, _ = which_one_of(translate(op.left.type()), "kind")
    right_type, _ = which_one_of(translate(op.right.type()), "kind")
    op_class = "scalar_functions"
    op_name = IBIS_SUBSTRAIT_OP_MAPPING[type(op).__name__]
    type_signature = (
        "_".join((left_type, right_type))
        if not FUNCTION_SIGNATURES[op_class][op_name]["variadic"]
        else left_type
    )
    any_sig = "any1_any1"

    return op_class, type_signature, any_sig


@op_signature.register
def _reduction(op: ops.Reduction) -> tuple[str, str, str]:
    from .translate import translate

    left_type, _ = which_one_of(translate(op.output_dtype), "kind")
    op_class = "aggregate_functions"
    type_signature = left_type
    any_sig = "any1"

    return op_class, type_signature, any_sig


@op_signature.register
def _unary(op: ops.Unary) -> tuple[str, str, str]:
    from .translate import translate

    left_type, _ = which_one_of(translate(op.arg.type()), "kind")
    op_class = "scalar_functions"
    type_signature = left_type
    any_sig = "any1"

    return op_class, type_signature, any_sig


@op_signature.register
def _fuzzy(op: ops.FuzzySearch) -> tuple[str, str, str]:
    from .translate import translate

    left_type, _ = which_one_of(translate(op.arg.type()), "kind")
    pattern_type, _ = which_one_of(translate(op.pattern.type()), "kind")
    op_class = "scalar_functions"
    type_signature = "_".join((left_type, pattern_type))
    any_sig = "any1"

    return op_class, type_signature, any_sig


@op_signature.register
def _substring(op: ops.Substring) -> tuple[str, str, str]:
    from .translate import translate

    left_type, _ = which_one_of(translate(op.arg.type()), "kind")
    start_type, _ = which_one_of(translate(op.start.type()), "kind")
    length_type, _ = which_one_of(translate(op.length.type()), "kind")
    op_class = "scalar_functions"
    type_signature = "_".join((left_type, start_type, length_type))
    any_sig = "any1_any1_any1"

    return op_class, type_signature, any_sig


@op_signature.register
def _between(op: ops.Between) -> tuple[str, str, str]:
    from .translate import translate

    left_type, _ = which_one_of(translate(op.arg.type()), "kind")
    lower_bound_type, _ = which_one_of(translate(op.lower_bound.type()), "kind")
    upper_bound_type, _ = which_one_of(translate(op.upper_bound.type()), "kind")
    op_class = "scalar_functions"
    type_signature = "_".join((left_type, lower_bound_type, upper_bound_type))
    any_sig = "any1_any1_any1"

    return op_class, type_signature, any_sig


def function_signature_lookup(op: ops.ValueOp) -> tuple[str, str]:

    op_name = IBIS_SUBSTRAIT_OP_MAPPING[type(op).__name__]
    op_class, type_signature, any_sig = op_signature(op)

    # function signatures keys are in the form:
    # scalar_function_left_type_right_type
    # aggregate_function_output_type
    try:
        extension_func_info = (
            FUNCTION_SIGNATURES[op_class][op_name].get(any_sig, False)
            or FUNCTION_SIGNATURES[op_class][op_name][f"{type_signature}"]
        )
    except KeyError:
        raise TypeError(
            f"Invalid type signature for extension function {op_name}: {type_signature}"
        )

    # return properly formed signature and extension yaml filename
    return (
        extension_func_info["extension_signature"],
        extension_func_info["extension_file"],
    )


class SubstraitCompiler:
    def __init__(self) -> None:
        """Initialize the compiler.

        Parameters
        ----------
        uri
            The extension URI to use, if any.
        """
        # start at id 1 because 0 is the default proto value for the type
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
        signature, filename = function_signature_lookup(op)
        try:
            function_extension = self.function_extensions[signature]
        except KeyError:
            try:
                extension_uri = self.extension_uris[filename]
            except KeyError:
                extension_uri = self.extension_uris[filename] = ste.SimpleExtensionURI(
                    extension_uri_anchor=len(self.extension_uris) + 1, uri=filename
                )
            function_extension = self.function_extensions[
                signature
            ] = ste.SimpleExtensionDeclaration.ExtensionFunction(
                extension_uri_reference=extension_uri.extension_uri_anchor,
                function_anchor=next(self.id_generator),
                name=signature,
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
