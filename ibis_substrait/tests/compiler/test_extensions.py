import operator

import ibis
import ibis.expr.operations as ops
import pytest

DEFAULT_PREFIX = "https://github.com/substrait-io/substrait/blob/main/extensions"


@pytest.mark.parametrize(
    "two, three",
    [
        (2, 3),
        (ibis.literal(2, "int32"), ibis.literal(3, "int32")),
        (ibis.literal(2, "int32"), ibis.literal(3, "int64")),
        (ibis.literal(2, "int16"), ibis.literal(3, "int8")),
    ],
)
def test_extension_substring(compiler, two, three):
    t = ibis.table([("one", "string"), ("two", "float"), ("three", "int32")], name="t")

    query = t[t.one == t.one.substr(two, three)]
    plan = compiler.compile(query)

    scalar_func_names = [
        extension.extension_function.name for extension in plan.extensions
    ]

    uris = [ext.uri for ext in plan.extension_uris]

    assert "equal:any_any" in scalar_func_names
    assert "substring:str_i32_i32" in scalar_func_names

    assert f"{DEFAULT_PREFIX}/functions_comparison.yaml" in uris
    assert f"{DEFAULT_PREFIX}/functions_string.yaml" in uris


@pytest.mark.parametrize(
    "left, right, bin_op, exp_func",
    [
        ("int32", "int32", operator.gt, "gt:any_any"),
        ("int32", "int64", operator.lt, "lt:any_any"),
        ("int16", "int8", operator.ge, "gte:any_any"),
        ("float64", "int8", operator.le, "lte:any_any"),
        ("float64", "float32", operator.eq, "equal:any_any"),
        ("int8", "float64", operator.ne, "not_equal:any_any"),
    ],
)
def test_extension_binop_comparison(compiler, left, right, bin_op, exp_func):
    t = ibis.table([("left", left), ("right", right)], name="t")

    query = t[bin_op(t.left, t.right)]
    plan = compiler.compile(query)

    scalar_func_names = [
        extension.extension_function.name for extension in plan.extensions
    ]

    uris = [ext.uri for ext in plan.extension_uris]

    assert exp_func in scalar_func_names

    assert f"{DEFAULT_PREFIX}/functions_comparison.yaml" in uris


@pytest.mark.parametrize(
    "left, unary_op, exp_func",
    [
        ("int32", ops.NotNull, "is_not_null"),
        ("string", ops.IsNull, "is_null"),
        ("float64", ops.IsInf, "is_infinite"),
        ("float32", ops.IsNan, "is_nan"),
    ],
)
def test_extension_unaryop_comparison(compiler, left, unary_op, exp_func):
    t = ibis.table([("left", left)], name="t")

    query = t[unary_op(t.left).to_expr()]
    plan = compiler.compile(query)

    scalar_func_names = [
        extension.extension_function.name for extension in plan.extensions
    ]

    uris = [ext.uri for ext in plan.extension_uris]

    assert any(exp_func in func_name for func_name in scalar_func_names)

    assert f"{DEFAULT_PREFIX}/functions_comparison.yaml" in uris


@pytest.mark.parametrize(
    "left, right, bin_op, exp_func, exp_uri",
    [
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.add,
            "add:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.sub,
            "subtract:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.mul,
            "multiply:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.truediv,
            "divide:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "int",
            operator.add,
            # should promote to dec_dec from dec_int
            "add:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "float64",
            "decimal(15, 3)",
            operator.sub,
            # should promote to dec_dec from fp32_dec
            "subtract:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "int32",
            operator.mul,
            # should promote to dec_dec from dec_int
            "multiply:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "float32",
            "decimal(15, 3)",
            operator.truediv,
            # should promote to dec_dec from fp32_dec
            "divide:dec_dec",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "int",
            "int8",
            operator.add,
            # int is shorthand for i64, should promote to i64_i64
            "add:i64_i64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "int32",
            "int",
            operator.sub,
            # int is shorthand for i64, should promote to i64_i64
            "subtract:i64_i64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "int64",
            "int",
            operator.mul,
            # int is shorthand for i64, should promote to i64_i64
            "multiply:i64_i64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "int",
            "int",
            operator.truediv,
            "divide:i64_i64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float64",
            "float",
            operator.add,
            "add:fp64_fp64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float",
            "float32",
            operator.sub,
            # float is shorthand for fp64, should promote to fp64_fp64
            "subtract:fp64_fp64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float32",
            "float32",
            operator.sub,
            "subtract:fp32_fp32",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float64",
            "float64",
            operator.mul,
            "multiply:fp64_fp64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float",
            "float",
            operator.truediv,
            "divide:fp64_fp64",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
    ],
)
def test_extension_arithmetic(compiler, left, right, bin_op, exp_func, exp_uri):
    t = ibis.table([("left", left), ("right", right)], name="t")

    query = t.mutate(new=bin_op(t.left, t.right))
    plan = compiler.compile(query)

    scalar_func_names = [
        extension.extension_function.name for extension in plan.extensions
    ]

    uris = [ext.uri for ext in plan.extension_uris]

    assert exp_func in scalar_func_names

    assert exp_uri in uris


@pytest.mark.parametrize(
    "left, right, bin_op, exp_func, exp_uri",
    [
        (
            "bool",
            "bool",
            operator.and_,
            "and:bool",  # `and` is variadic with minimum 0 args so
            # expected signature is a single `bool`
            f"{DEFAULT_PREFIX}/functions_boolean.yaml",
        ),
        (
            "bool",
            "bool",
            operator.or_,
            "or:bool",  # `or` is variadic with minimum 0 args so
            # expected signature is a single `bool`
            f"{DEFAULT_PREFIX}/functions_boolean.yaml",
        ),
    ],
)
def test_extension_boolean(compiler, left, right, bin_op, exp_func, exp_uri):
    t = ibis.table([("left", left), ("right", right)], name="t")

    query = t.mutate(new=bin_op(t.left, t.right))
    plan = compiler.compile(query)

    scalar_func_names = [
        extension.extension_function.name for extension in plan.extensions
    ]

    uris = [ext.uri for ext in plan.extension_uris]

    assert exp_func in scalar_func_names

    assert exp_uri in uris


def test_extension_udf_compile(compiler):
    try:
        from ibis.udf.vectorized import elementwise
    except ImportError:
        from ibis.legacy.udf.vectorized import elementwise

    pc = None

    t = ibis.table([("a", "int")], name="t")

    @elementwise(input_type=["int64"], output_type="int64")
    def add1(col, ctx=None):
        return pc.call_function("add", [col, 1], memory_pool=ctx.memory_pool)

    @elementwise(input_type=["int64"], output_type="int64")
    def sub1(col, ctx=None):
        return pc.call_function("subtract", [col, 1], memory_pool=ctx.memory_pool)

    query = t.mutate(b=add1(t.a), c=sub1(t.a))

    with pytest.raises(ValueError, match="udf_uri"):
        plan = compiler.compile(query)

    compiler.udf_uri = "orkbork"

    plan = compiler.compile(query)

    assert plan.extension_uris[0].uri == "orkbork"
    assert len(plan.extensions) == 2
    assert plan.extensions[0].extension_function.name == "add1"
    assert plan.extensions[1].extension_function.name == "sub1"


def test_extension_register_uri_override(tmp_path):
    from ibis_substrait.compiler.mapping import (
        _extension_mapping,
        register_extension_yaml,
    )

    sample_yaml = """scalar_functions:
  -
    name: "anotheradd"
    impls:
      - args:
          - name: x
            value: a
          - name: y
            value: b
        return: c"""

    yaml_file = tmp_path / "foo.yaml"
    yaml_file.write_text(sample_yaml)

    register_extension_yaml(yaml_file, uri="orkbork")

    assert _extension_mapping["anotheradd"]
    assert _extension_mapping["anotheradd"][("a", "b")].uri == "orkbork"

    register_extension_yaml(yaml_file, prefix="orkbork")
    assert _extension_mapping["anotheradd"]
    assert _extension_mapping["anotheradd"][("a", "b")].uri == "orkbork/foo.yaml"


def test_extension_arithmetic_multiple_signatures(compiler):
    t = ibis.table([("left", "int64"), ("right", "float32")], name="t")

    query = t.mutate(
        intadd=t.left + t.left,
        floatadd=t.right + t.right,
        intsub=t.left - t.left,
        floatsub=t.right - t.right,
    )
    plan = compiler.compile(query)

    scalar_func_names = [
        extension.extension_function.name for extension in plan.extensions
    ]

    assert "add:i64_i64" in scalar_func_names
    assert "add:fp32_fp32" in scalar_func_names
    assert "subtract:i64_i64" in scalar_func_names
    assert "subtract:fp32_fp32" in scalar_func_names


_TYPE_MAPPING = {
    "int8": "i8",
    "int16": "i16",
    "int32": "i32",
    "int64": "i64",
    "float32": "fp32",
    "float64": "fp64",
}


@pytest.mark.parametrize(
    "col_dtype", ["float32", "float64", "int8", "int16", "int32", "int64"]
)
@pytest.mark.parametrize("digits_dtype", ["int8", "int16", "int32", "int64"])
def test_extension_round_upcast(compiler, col_dtype, digits_dtype):
    t = ibis.table([("col", col_dtype)], name="t")

    query = t.mutate(col=t.col.round(ibis.literal(8, type=digits_dtype)))
    plan = compiler.compile(query)

    scalar_func_names = [
        extension.extension_function.name for extension in plan.extensions
    ]

    assert f"round:{_TYPE_MAPPING[col_dtype]}_i32" in scalar_func_names


def test_ops_mapping_validity():
    from ibis_substrait.compiler.mapping import (
        IBIS_SUBSTRAIT_OP_MAPPING,
        _extension_mapping,
    )

    for op in IBIS_SUBSTRAIT_OP_MAPPING.keys():
        assert hasattr(ops, op)

    # `any` isn't a valid mapping
    for target in IBIS_SUBSTRAIT_OP_MAPPING.values():
        if target == "any":
            # any is special-cased
            continue
        assert target in _extension_mapping.keys()
