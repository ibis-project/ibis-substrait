from __future__ import annotations

import importlib.resources
from collections import defaultdict
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

import ibis.expr.operations as ops
import yaml

IBIS_SUBSTRAIT_OP_MAPPING = {
    "Abs": "abs",
    "Acos": "acos",
    "Add": "add",
    "And": "and",
    "Any": "any",
    "ApproxCountDistinct": "approx_count_distinct",
    "ApproxMedian": "median",
    "Asin": "asin",
    "Atan": "atan",
    "Atan2": "atan2",
    "BitAnd": "bitwise_and",
    "BitOr": "bitwise_or",
    "BitXor": "bitwise_xor",
    "Between": "between",
    "Capitalize": "capitalize",
    "Ceil": "ceil",
    "Coalesce": "coalesce",
    "Cos": "cos",
    "Count": "count",
    "CountStar": "count",
    "CountDistinct": "count",
    "Divide": "divide",
    "SubstraitDivide": "divide",
    "EndsWith": "ends_with",
    "Equals": "equal",
    "Exp": "exp",
    "ExtractYear": "extract",
    "ExtractMonth": "extract",
    "ExtractDay": "extract",
    "Floor": "floor",
    "Greater": "gt",
    "GreaterEqual": "gte",
    "IsInf": "is_infinite",
    "IsNan": "is_nan",
    "IsNull": "is_null",
    "Less": "lt",
    "LessEqual": "lte",
    "Ln": "ln",
    "Log": "logb",
    "Log2": "log2",
    "Log10": "log10",
    "Lowercase": "lower",
    "LPad": "lpad",
    "LStrip": "ltrim",
    "Max": "max",
    "Mean": "avg",
    "Min": "min",
    "Modulus": "modulus",
    "Multiply": "multiply",
    "Negate": "negate",
    "Not": "not",
    "NotEquals": "not_equal",
    "NotNull": "is_not_null",
    "NullIf": "nullif",
    "Or": "or",
    "Power": "power",
    "RegexExtract": "regexp_match_substring",
    "RegexReplace": "regexp_replace",
    "Repeat": "repeat",
    "Reverse": "reverse",
    "SubstraitRound": "round",
    "Round": "round",
    "RPad": "rpad",
    "RStrip": "rtrim",
    "Sign": "sign",
    "Sin": "sin",
    "Sqrt": "sqrt",
    "StandardDev": "std_dev",
    "StartsWith": "starts_with",
    "StringFind": "strpos",
    "StringConcat": "concat",
    "StringContains": "contains",
    "StringLength": "char_length",
    "StringReplace": "replace",
    "StringSplit": "string_split",
    "StringSQLLike": "like",
    "Strip": "trim",
    "StrRight": "right",
    "Substring": "substring",
    "Subtract": "subtract",
    "Sum": "sum",
    "Tan": "tan",
    "Uppercase": "upper",
    "Variance": "variance",
    "Xor": "xor",
}

SUBSTRAIT_IBIS_OP_MAPPING = {
    v: getattr(ops, k) for k, v in IBIS_SUBSTRAIT_OP_MAPPING.items() if hasattr(ops, k)
}
# override when reversing many-to-one mappings
SUBSTRAIT_IBIS_OP_MAPPING["extract"] = lambda span, table: getattr(
    ops, f"Extract{span.capitalize()}"
)(table)


IBIS_SUBSTRAIT_TYPE_MAPPING = {
    "Int8": "i8",
    "Int16": "i16",
    "Int32": "i32",
    "Int64": "i64",
    "Float32": "fp32",
    "Float64": "fp64",
    "String": "str",
    "string": "str",
    "Boolean": "bool",
    "Date": "date",
    "Decimal": "dec",
}

_normalized_key_names = {
    "binary": "vbin",
    "interval_compound": "icompound",
    "interval_day": "iday",
    "interval_year": "iyear",
    "string": "str",
    "timestamp": "ts",
    "timestamp_tz": "tstz",
}


def normalize_substrait_type_names(typ: str) -> str:
    # First strip off any punctuation
    typ = typ.strip("?").lower()

    # Common prefixes whose information does not matter to an extension function
    # signature
    for complex_type, abbr in [
        ("fixedchar", "fchar"),
        ("varchar", "vchar"),
        ("fixedbinary", "fbin"),
        ("decimal", "dec"),
        ("precision_timestamp", "pts"),
        ("precision_timestamp_tz", "ptstz"),
        ("struct", "struct"),
        ("list", "list"),
        ("map", "map"),
        ("any", "any"),
        ("boolean", "bool"),
        # Absolute garbage type info
        ("decimal", "dec"),
        ("delta", "dec"),
        ("prec", "dec"),
        ("scale", "dec"),
        ("init_", "dec"),
        ("min_", "dec"),
        ("max_", "dec"),
    ]:
        if typ.lower().startswith(complex_type):
            typ = abbr

    # Then pass through the dictionary of mappings, defaulting to just the
    # existing string
    typ = _normalized_key_names.get(typ.lower(), typ.lower())
    return typ


_extension_mapping: Mapping[str, Any] = defaultdict(dict)


class FunctionEntry:
    def __init__(self, name: str) -> None:
        self.name = name
        self.options: Mapping[str, Any] = {}
        self.arg_names: list = []
        self.inputs: list = []
        self.uri: str = ""

    def parse(self, impl: Mapping[str, Any]) -> None:
        self.rtn = normalize_substrait_type_names(impl["return"])
        self.nullability = impl.get("nullability", False)
        self.variadic = impl.get("variadic", False)
        if input_args := impl.get("args", []):
            for val in input_args:
                if typ := val.get("value"):
                    typ = normalize_substrait_type_names(typ)
                    self.inputs.append(typ)
                elif arg_name := val.get("name", None):
                    self.arg_names.append(arg_name)

        if options_args := impl.get("options", []):
            for val in options_args:
                self.options[val] = options_args[val]["values"]  # type: ignore

    def __repr__(self) -> str:
        return f"{self.name}:{'_'.join(self.inputs)}"

    def castable(self) -> None:
        raise NotImplementedError


def _parse_func(entry: Mapping[str, Any]) -> Iterator[FunctionEntry]:
    for impl in entry.get("impls", []):
        sf = FunctionEntry(entry["name"])
        sf.parse(impl)

        yield sf


def register_extension_yaml(
    fname: str | Path, prefix: str | None = None, uri: str | None = None
) -> None:
    """Add a substrait extension YAML file to the ibis substrait compiler.

    Parameters
    ----------
    fname
        The filename of the extension yaml to register.
    prefix
        Custom prefix to use when constructing Substrait extension URI
    uri
        A custom URI to use for all functions defined within `fname`.
        If passed, this value overrides `prefix`.


    """
    fname = Path(fname)
    with open(fname) as f:  # type: ignore
        extension_definitions = yaml.safe_load(f)

    prefix = (
        prefix.strip("/")
        if prefix is not None
        else "https://github.com/substrait-io/substrait/blob/main/extensions"
    )

    for named_functions in extension_definitions.values():
        for function in named_functions:
            for func in _parse_func(function):
                func.uri = uri or f"{prefix}/{fname.name}"
                _extension_mapping[function["name"]][(tuple(func.inputs), func.rtn)] = (
                    func
                )


def _populate_default_extensions() -> None:
    for fpath in importlib.resources.files("substrait.extensions").glob(  # type: ignore
        "functions*.yaml"
    ):
        register_extension_yaml(fpath)


_populate_default_extensions()
