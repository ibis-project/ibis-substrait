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

    assert "equal" in scalar_func_names
    assert "substring" in scalar_func_names

    assert f"{DEFAULT_PREFIX}/functions_comparison.yaml" in uris
    assert f"{DEFAULT_PREFIX}/functions_string.yaml" in uris


@pytest.mark.parametrize(
    "left, right, bin_op, exp_func",
    [
        ("int32", "int32", operator.gt, "gt"),
        ("int32", "int64", operator.lt, "lt"),
        ("int16", "int8", operator.ge, "gte"),
        ("float64", "int8", operator.le, "lte"),
        ("float64", "float32", operator.eq, "equal"),
        ("int8", "float64", operator.ne, "not_equal"),
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

    assert exp_func in scalar_func_names

    assert f"{DEFAULT_PREFIX}/functions_comparison.yaml" in uris


@pytest.mark.parametrize(
    "left, right, bin_op, exp_func, exp_uri",
    [
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.add,
            "add",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.sub,
            "subtract",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.mul,
            "multiply",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "decimal(15, 3)",
            operator.truediv,
            "divide",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "int",
            operator.add,
            "add",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "float64",
            "decimal(15, 3)",
            operator.sub,
            "subtract",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "decimal(15, 3)",
            "int32",
            operator.mul,
            "multiply",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "float32",
            "decimal(15, 3)",
            operator.truediv,
            "divide",
            f"{DEFAULT_PREFIX}/functions_arithmetic_decimal.yaml",
        ),
        (
            "int",
            "int8",
            operator.add,
            "add",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "int32",
            "int",
            operator.sub,
            "subtract",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "int64",
            "int",
            operator.mul,
            "multiply",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "int",
            "int",
            operator.truediv,
            "divide",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float64",
            "float",
            operator.add,
            "add",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float",
            "float32",
            operator.sub,
            "subtract",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float64",
            "float64",
            operator.mul,
            "multiply",
            f"{DEFAULT_PREFIX}/functions_arithmetic.yaml",
        ),
        (
            "float",
            "float",
            operator.truediv,
            "divide",
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
            "and",
            f"{DEFAULT_PREFIX}/functions_boolean.yaml",
        ),
        (
            "bool",
            "bool",
            operator.or_,
            "or",
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
    from ibis.udf.vectorized import elementwise

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
