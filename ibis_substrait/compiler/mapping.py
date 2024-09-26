from __future__ import annotations

from ibis.expr.datatypes.core import DataType

IBIS_SUBSTRAIT_OP_MAPPING: dict[str, list[tuple[str]]] = {
    "Abs": [("functions_arithmetic.yaml", "abs")],
    "Acos": [("functions_arithmetic.yaml", "acos")],
    "Add": [
        ("functions_arithmetic.yaml", "add"),
        ("functions_arithmetic_decimal.yaml", "add"),
    ],
    "And": [("functions_boolean.yaml", "and")],
    # "Any": "any",
    "ApproxCountDistinct": [("functions_aggregate_approx", "approx_count_distinct")],
    "ApproxMedian": [("functions_arithmetic.yaml", "median")],
    "Asin": [("functions_arithmetic.yaml", "asin")],
    "Atan": [("functions_arithmetic.yaml", "atan")],
    "Atan2": [("functions_arithmetic.yaml", "atan2")],
    "BitAnd": [("functions_arithmetic.yaml", "bitwise_and")],
    "BitOr": [("functions_arithmetic.yaml", "bitwise_or")],
    "BitXor": [("functions_arithmetic.yaml", "bitwise_xor")],
    "Between": [("functions_comparison.yaml", "between")],
    "Capitalize": [("functions_string.yaml", "capitalize")],
    "Ceil": [("functions_rounding.yaml", "ceil")],
    "Coalesce": [("functions_comparison.yaml", "coalesce")],
    "Cos": [("functions_arithmetic.yaml", "cos")],
    "Count": [("functions_aggregate_generic.yaml", "count")],
    "CountStar": [("functions_aggregate_generic.yaml", "count")],
    "CountDistinct": [("functions_aggregate_generic.yaml", "count")],
    "Divide": [
        ("functions_arithmetic.yaml", "divide"),
        ("functions_arithmetic_decimal.yaml", "divide"),
    ],
    "SubstraitDivide": [
        ("functions_arithmetic.yaml", "divide"),
        ("functions_arithmetic_decimal.yaml", "divide"),
    ],
    "EndsWith": [("functions_string.yaml", "ends_with")],
    "Equals": [("functions_comparison.yaml", "equal")],
    "Exp": [("functions_arithmetic.yaml", "exp")],
    "ExtractYear": [("functions_datetime.yaml", "extract")],
    "ExtractMonth": [("functions_datetime.yaml", "extract")],
    "ExtractDay": [("functions_datetime.yaml", "extract")],
    "Floor": [("functions_rounding.yaml", "floor")],
    "Greater": [("functions_comparison.yaml", "gt")],
    "GreaterEqual": [("functions_comparison.yaml", "gte")],
    "IsInf": [("functions_comparison.yaml", "is_infinite")],
    "IsNan": [("functions_comparison.yaml", "is_nan")],
    "IsNull": [("functions_comparison.yaml", "is_null")],
    "Less": [("functions_comparison.yaml", "lt")],
    "LessEqual": [("functions_comparison.yaml", "lte")],
    "Ln": [("functions_logarithmic.yaml", "ln")],
    "Log": [("functions_logarithmic.yaml", "logb")],
    "Log2": [("functions_logarithmic.yaml", "log2")],
    "Log10": [("functions_logarithmic.yaml", "log10")],
    "Lowercase": [("functions_string.yaml", "lower")],
    "LPad": [("functions_string.yaml", "lpad")],
    "LStrip": [("functions_string.yaml", "ltrim")],
    "Max": [
        ("functions_arithmetic.yaml", "max"),
        ("functions_arithmetic_decimal.yaml", "max"),
    ],
    "Mean": [
        ("functions_arithmetic.yaml", "avg"),
        ("functions_arithmetic_decimal.yaml", "avg"),
    ],
    "Min": [
        ("functions_arithmetic.yaml", "min"),
        ("functions_arithmetic_decimal.yaml", "min"),
    ],
    "Modulus": [("functions_arithmetic.yaml", "modulus")],
    "Multiply": [
        ("functions_arithmetic.yaml", "multiply"),
        ("functions_arithmetic_decimal.yaml", "multiply"),
    ],
    "Negate": [("functions_arithmetic.yaml", "negate")],
    "Not": [("functions_boolean.yaml", "not")],
    "NotEquals": [("functions_comparison.yaml", "not_equal")],
    "NotNull": [("functions_comparison.yaml", "is_not_null")],
    "NullIf": [("functions_comparison.yaml", "nullif")],
    "Or": [("functions_boolean.yaml", "or")],
    "Power": [("functions_arithmetic.yaml", "power")],
    "RegexExtract": [("functions_string.yaml", "regexp_match_substring")],
    "RegexReplace": [("functions_string.yaml", "regexp_replace")],
    "Repeat": [("functions_string.yaml", "repeat")],
    "Reverse": [("functions_string.yaml", "reverse")],
    "SubstraitRound": [("functions_rounding.yaml", "round")],
    "Round": [("functions_rounding.yaml", "round")],
    "RPad": [("functions_string.yaml", "rpad")],
    "RStrip": [("functions_string.yaml", "rtrim")],
    "Sign": [("functions_arithmetic.yaml", "sign")],
    "Sin": [("functions_arithmetic.yaml", "sin")],
    "Sqrt": [("functions_arithmetic.yaml", "sqrt")],
    "StandardDev": [("functions_arithmetic.yaml", "std_dev")],
    "StartsWith": [("functions_string.yaml", "starts_with")],
    "StringFind": [("functions_string.yaml", "strpos")],
    "StringConcat": [("functions_string.yaml", "concat")],
    "StringContains": [("functions_string.yaml", "contains")],
    "StringLength": [("functions_string.yaml", "char_length")],
    "StringReplace": [("functions_string.yaml", "replace")],
    "StringSplit": [("functions_string.yaml", "string_split")],
    "StringSQLLike": [("functions_string.yaml", "like")],
    "Strip": [("functions_string.yaml", "trim")],
    "StrRight": [("functions_string.yaml", "right")],
    "Substring": [("functions_string.yaml", "substring")],
    "Subtract": [
        ("functions_arithmetic.yaml", "subtract"),
        ("functions_arithmetic_decimal.yaml", "subtract"),
    ],
    "Sum": [
        ("functions_arithmetic.yaml", "sum"),
        ("functions_arithmetic_decimal.yaml", "sum"),
    ],
    "Tan": [("functions_arithmetic.yaml", "tan")],
    "Uppercase": [("functions_string.yaml", "upper")],
    "Variance": [("functions_arithmetic.yaml", "variance")],
    "Xor": [("functions_boolean.yaml", "xor")],
}

IBIS_SUBSTRAIT_TYPE_MAPPING = {
    "Int8": "i8",
    "Int16": "i16",
    "Int32": "i32",
    "Int64": "i64",
    "Float32": "fp32",
    "Float64": "fp64",
    "String": "string",
    "Boolean": "boolean",
    "Date": "date",
}


def ibis_type_to_substrait(dtype: DataType) -> str:
    if dtype.name == "Decimal":
        return f"decimal<{dtype.precision},{dtype.scale}>"
    else:
        return IBIS_SUBSTRAIT_TYPE_MAPPING[dtype.name]


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
