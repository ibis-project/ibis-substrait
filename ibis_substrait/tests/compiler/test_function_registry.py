import yaml

from ibis_substrait.compiler.function_registry import FunctionRegistry

content = """%YAML 1.2
---
scalar_functions:
  - name: "test_fn"
    description: ""
    impls:
      - args:
          - value: i8
        variadic:
          min: 2
        return: i8
  - name: "test_fn_variadic_any"
    description: ""
    impls:
      - args:
          - value: any1
        variadic:
          min: 2
        return: any1
  - name: "add"
    description: "Add two values."
    impls:
      - args:
          - name: x
            value: i8
          - name: y
            value: i8
        options:
          overflow:
            values: [ SILENT, SATURATE, ERROR ]
        return: i8
      - args:
          - name: x
            value: i8
          - name: y
            value: i8
          - name: z
            value: any
        options:
          overflow:
            values: [ SILENT, SATURATE, ERROR ]
        return: i16
      - args:
          - name: x
            value: any1
          - name: y
            value: any1
          - name: z
            value: any2
        options:
          overflow:
            values: [ SILENT, SATURATE, ERROR ]
        return: any2
  - name: "test_decimal"
    impls:
      - args:
          - name: x
            value: decimal<P1,S1>
          - name: y
            value: decimal<S1,S2>
        return: decimal<P1,S2>

"""


registry = FunctionRegistry()

registry.register_extension_dict(yaml.safe_load(content), uri="test")


def test_non_existing_uri():
    assert (
        registry.lookup_function(
            uri="non_existent", function_name="add", signature=["i8", "i8"]
        )
        is None
    )


def test_non_existing_function():
    assert (
        registry.lookup_function(
            uri="test", function_name="sub", signature=["i8", "i8"]
        )
        is None
    )


def test_non_existing_function_signature():
    assert (
        registry.lookup_function(uri="test", function_name="add", signature=["i8"])
        is None
    )


def test_exact_match():
    assert (
        registry.lookup_function(
            uri="test", function_name="add", signature=["i8", "i8"]
        )[1]
        == "i8"
    )


def test_wildcard_match():
    assert (
        registry.lookup_function(
            uri="test", function_name="add", signature=["i8", "i8", "bool"]
        )[1]
        == "i16"
    )


def test_wildcard_match_fails_with_constraits():
    assert (
        registry.lookup_function(
            uri="test", function_name="add", signature=["i8", "i16", "i16"]
        )
        is None
    )


def test_wildcard_match_with_constraits():
    assert (
        registry.lookup_function(
            uri="test", function_name="add", signature=["i16", "i16", "i8"]
        )[1]
        == "i8"
    )


def test_variadic():
    assert (
        registry.lookup_function(
            uri="test", function_name="test_fn", signature=["i8", "i8", "i8"]
        )[1]
        == "i8"
    )


def test_variadic_any():
    assert (
        registry.lookup_function(
            uri="test",
            function_name="test_fn_variadic_any",
            signature=["i16", "i16", "i16"],
        )[1]
        == "i16"
    )


def test_variadic_fails_min_constraint():
    assert (
        registry.lookup_function(uri="test", function_name="test_fn", signature=["i8"])
        is None
    )


def test_decimal_happy_path():
    assert (
        registry.lookup_function(
            uri="test",
            function_name="test_decimal",
            signature=["decimal<10,8>", "decimal<8,6>"],
        )[1]
        == "decimal<10,6>"
    )


def test_decimal_violates_constraint():
    assert (
        registry.lookup_function(
            uri="test",
            function_name="test_decimal",
            signature=["decimal<10,8>", "decimal<12,10>"],
        )
        is None
    )
