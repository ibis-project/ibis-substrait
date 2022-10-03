from __future__ import annotations

import importlib.resources
from collections import defaultdict
from typing import Any, Mapping

import ibis.expr.operations as ops
import yaml

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
    "Mean": "sum",
    "Min": "min",
    "Multiply": "multiply",
    "Not": "not",
    "NotEquals": "not_equal",
    "Or": "or",
    "StringLength": "char_length",
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

EXTENSION_YAMLS = [
    "functions_boolean.yaml",
    "functions_string.yaml",
    "functions_aggregate_approx.yaml",
    "functions_comparison.yaml",
    "functions_aggregate_generic.yaml",
    "functions_datetime.yaml",
    "functions_arithmetic.yaml",
    "functions_logarithmic.yaml",
    "functions_arithmetic_decimal.yaml",
    "functions_rounding.yaml",
]


def _extract_input_types(entry: Mapping[str, Any]) -> Mapping[str, Any]:
    args: Any = defaultdict(list)
    args["return"] = entry["return"]
    args["variadic"] = entry.get("variadic", False)
    for val in entry["args"]:
        if typ := val.get("value", None):
            args["inputs"].append(typ)
        elif arg_name := val.get("name", None):
            args["arg_names"].append(arg_name)
        else:
            args = {**args, **val}

    return args


def _generate_extension_signature(
    func_name: str,
    args: Mapping[str, Any],
) -> str:
    """Generate an extension function signature."""
    if "options" in args.keys():
        typs = ["opt"] + args["inputs"]
    else:
        typs = args["inputs"]

    # remove trailing question mark from extension signature
    return f"{func_name}:{'_'.join((typ.strip('?') for typ in typs))}"


def _normalize_key_name(key: str) -> str:
    """Horrible hacks"""
    # MORE HACKS
    # hilarious inconsistency
    key = key.replace("DECIMAL", "decimal")
    # hilarious inconsistency
    key = key.replace("boolean?", "bool")
    # decimal precision and scale aren't part of the
    # extension signature they're passed in separately
    key = key.replace("<P, S>", "")
    key = key.replace("<P1,S1>", "")
    key = key.replace("<P2,S2>", "")
    # we don't care about string length
    key = key.replace("<L1>", "")
    key = key.replace("<l1>", "")
    key = key.replace("<L2>", "")

    return key


def _function_signature_dict() -> Mapping[str, Any]:
    """
    Yes, this is horrible.

    We build up a dictionary of all of the extension functions with the
    following structure:

    [function_class]      # one of scalar, aggregate, or window
     ↳
      [function_name]     # name of function, e.g. `add` or `sum`
        ↳
         ["variadic"]     # defaults to None, otherwise min # of arguments
         [input_types_0]
         [input_types_1]  # e.g. `i8_i8`, or `fp64_fp64`
         [...]
         [input_types_n]

    """
    extension_dir = importlib.resources.files("ibis_substrait") / "extensions"
    # Create a nested defaultdict
    func_dict: Any = defaultdict(lambda: defaultdict(dict))
    for yaml_file in EXTENSION_YAMLS:
        with open(extension_dir / yaml_file) as f:  # type: ignore
            extension_definitions = yaml.safe_load(f)

            # func_class resolves to one of scalar, aggregate, or window
            # funcs is a list of the named functions with their options + input
            # types
            for func_class, func_list in extension_definitions.items():
                for func in func_list:
                    name = func["name"]
                    # Rip out the list of accepted inputs
                    func_info = list(map(_extract_input_types, func["impls"]))
                    for entry in func_info:
                        func_dict[func_class][name]["variadic"] = entry["variadic"]
                        # Some extensions don't define any explicit inputs and
                        # accept any inputs for those we use the key "any"
                        key = "_".join(entry["inputs"]) or "any1"

                        key = _normalize_key_name(key)

                        func_dict[func_class][name][key] = {
                            "extension_signature": _generate_extension_signature(
                                name, entry
                            ),
                            "extension_file": str(yaml_file),
                        }

    return func_dict


FUNCTION_SIGNATURES = _function_signature_dict()
