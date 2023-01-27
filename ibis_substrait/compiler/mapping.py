from __future__ import annotations

import importlib.resources
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterator, Mapping

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
    "CountDistinct": "countdistinct",
    "Divide": "divide",
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
    "Round": "round",
    "RPad": "rpad",
    "RStrip": "rtrim",
    "Sign": "sign",
    "Sin": "sin",
    "Sqrt": "sqrt",
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
    "String": "varchar",
    "string": "string",
    "Boolean": "boolean",
    "Date": "date",
    "Decimal": "decimal",
}

_normalized_key_names = {
    # decimal precision and scale aren't part of the
    # extension signature they're passed in separately
    "decimal<p, s>": "decimal",
    "decimal<p,s>": "decimal",
    "decimal<p1,s1>": "decimal",
    "decimal<p2,s2>": "decimal",
    # we don't care about string length
    "fixedchar<l1>": "fixedchar",
    "fixedchar<l2>": "fixedchar",
    "varchar<l1>": "varchar",
    "varchar<l2>": "varchar",
    "varchar<l3>": "varchar",
    # for now ignore nullability marker
    "boolean?": "boolean",
    # why is there a 1?
    "any1": "any",
    "Date": "date",
}


_extension_mapping: Mapping[str, Any] = defaultdict(dict)


class FunctionEntry:
    def __init__(self, name: str) -> None:
        self.name = name
        self.options: Mapping[str, Any] = {}
        self.arg_names: list = []
        self.inputs: list = []
        self.uri: str = ""

    def parse(self, impl: Mapping[str, Any]) -> None:
        self.rtn = impl["return"]
        self.nullability = impl.get("nullability", False)
        self.variadic = impl.get("variadic", False)
        if input_args := impl.get("args", []):
            for val in input_args:
                if typ := val.get("value", None):
                    typ = _normalized_key_names.get(typ.lower(), typ.lower())
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
    for impl in entry["impls"]:
        sf = FunctionEntry(entry["name"])
        sf.parse(impl)

        yield sf


def register_extension_yaml(fname: str | Path, prefix: str | None = None) -> None:
    """Add a substrait extension YAML file to the ibis substrait compiler."""
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
                func.uri = f"{prefix}/{fname.name}"
                _extension_mapping[function["name"]][tuple(func.inputs)] = func


def _populate_default_extensions() -> None:
    # TODO: we should load all the yaml files and not maintain this list
    EXTENSION_YAMLS = [
        "functions_aggregate_approx.yaml",
        "functions_aggregate_generic.yaml",
        "functions_arithmetic.yaml",
        "functions_arithmetic_decimal.yaml",
        "functions_boolean.yaml",
        "functions_comparison.yaml",
        "functions_datetime.yaml",
        "functions_logarithmic.yaml",
        "functions_rounding.yaml",
        "functions_set.yaml",
        "functions_string.yaml",
    ]

    for yaml_file in EXTENSION_YAMLS:
        with importlib.resources.path("ibis_substrait.extensions", yaml_file) as fpath:
            register_extension_yaml(fpath)


_populate_default_extensions()
