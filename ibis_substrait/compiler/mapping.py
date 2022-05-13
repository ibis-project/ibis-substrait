IBIS_SUBSTRAIT_OP_MAPPING = {
    "Add": "+",  # wrong but using for duckdb compatibility right now
    "And": "and",
    "Any": "any",
    "Between": "between",
    "Cast": "cast",
    "Clip": "clip",
    "ClipLower": "clip_lower",
    "ClipUpper": "clip_upper",
    "Contains": "contains",
    "Count": "count",
    "CountDistinct": "countdistinct",
    "Divide": "/",  # wrong but using for duckdb compatibility right now
    "Equals": "equal",
    "ExtractYear": "extractyear",
    "Greater": "gt",
    "GreaterEqual": "gte",
    "Less": "lt",
    "LessEqual": "lte",
    "Max": "max",
    "Mean": "mean",
    "Min": "min",
    "Multiply": "*",  # wrong but using for duckdb compatibility right now
    "Negate": "negate",
    "Not": "not",
    "NotEquals": "not_equal",
    "Or": "or",
    "Power": "power",
    "StringLength": "string_length",  # don't know
    "StringSQLLike": "like",
    "Substring": "substring",
    "Subtract": "-",  # wrong but using for duckdb compatibility right now
    "Sum": "sum",
    "ValueList": "values",
}

SUBSTRAIT_IBIS_OP_MAPPING = {v: k for k, v in IBIS_SUBSTRAIT_OP_MAPPING.items()}
