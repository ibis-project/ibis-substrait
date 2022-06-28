import ibis.expr.operations as ops

IBIS_SUBSTRAIT_OP_MAPPING = {
    "Add": "add",
    "And": "and",
    "Any": "any",
    "Between": "between",
    "Count": "count",
    "CountDistinct": "countdistinct",
    "Divide": "divide",
    "Equals": "equal",
    "ExtractYear": "extract",
    "ExtractMonth": "extract",
    "ExtractDay": "extract",
    "Greater": "gt",
    "GreaterEqual": "gte",
    "Less": "lt",
    "LessEqual": "lte",
    "Max": "max",
    "Mean": "mean",
    "Min": "min",
    "Multiply": "multiply",
    "Not": "not",
    "NotEquals": "not_equal",
    "Or": "or",
    "StringLength": "string_length",  # don't know
    "StringSQLLike": "like",
    "Substring": "substring",
    "Subtract": "subtract",
    "Sum": "sum",
}

SUBSTRAIT_IBIS_OP_MAPPING = {
    v: getattr(ops, k) for k, v in IBIS_SUBSTRAIT_OP_MAPPING.items()
}
# override when reversing many-to-one mappings
SUBSTRAIT_IBIS_OP_MAPPING["extract"] = lambda span, table: getattr(
    ops, f"Extract{span.capitalize()}"
)(table)
