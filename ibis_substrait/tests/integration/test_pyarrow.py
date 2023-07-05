import ibis
import pytest
from packaging.version import parse as vparse

from ibis_substrait.compiler.core import SubstraitCompiler

pa = pytest.importorskip("pyarrow")
pc = pytest.importorskip("pyarrow.compute")
pa_substrait = pytest.importorskip("pyarrow.substrait")

try:
    from ibis.udf.vectorized import elementwise
except ImportError:
    from ibis.legacy.udf.vectorized import elementwise


arrow12 = pytest.mark.skipif(
    vparse(pa.__version__) <= vparse("11.0.0"),
    reason="UDF support added in Arrow 12",
)


def get_table_provider(tbl):
    """Create a table_provider that always returns tbl"""

    def table_provider(names, schema):
        return tbl

    return table_provider


def to_ibis_table(arrow_table, table_name="t1"):
    """Create ibis Table from pyarrow Table"""
    # TODO: use ibis.backends.pyarrow.datatypes.from_pyarrow_schema once we drop ibis 3.x
    return ibis.table(
        zip(arrow_table.schema.names, [str(type) for type in arrow_table.schema.types]),
        name=table_name,
    )


def run_query(plan, tbl):
    query_bytes = plan.SerializeToString()
    result = pa_substrait.run_query(
        # PyArrow wants its bytes in a very specific byte-string
        pa.py_buffer(query_bytes),
        table_provider=get_table_provider(tbl),
    )

    results = result.read_all()
    assert type(results) == pa.lib.Table

    return results


@pytest.fixture
def arrow_table():
    return pa.Table.from_pydict(
        {
            "a": [1, 2, 3],
            "b": [3.4, 3.7, 2.0],
            "c": ["x", "y", "z"],
            "d": [True, False, True],
        }
    )


@arrow12
def test_pyarrow_produces_correct_result(compiler, arrow_table):
    ibis_table = to_ibis_table(arrow_table)
    query = ibis_table  # identity
    plan = compiler.compile(query)
    result = run_query(plan, arrow_table)

    assert result == arrow_table


@arrow12
def test_pyarrow_can_consume_basic_operations(compiler, arrow_table):
    t = to_ibis_table(arrow_table)

    # identity
    query = t
    plan = compiler.compile(query)
    result = run_query(plan, arrow_table)
    assert result == arrow_table

    # mutate, re-use column
    query = t.mutate(a=t.a * 2)
    plan = compiler.compile(query)
    result = run_query(plan, arrow_table)

    assert set(result.column_names) == set(arrow_table.column_names)

    # mutate, add new derived column
    query = t.mutate(e=t.b + 1)
    plan = compiler.compile(query)
    result = run_query(plan, arrow_table)

    assert set(result.column_names) == {*arrow_table.column_names, "e"}


@arrow12
def test_extension_udf():
    def register_pyarrow_udf(udf, registry=None):
        """
        Boilerplate that is needed for the udfs to execute in PyArrow. Nothing to do with ibis.
        """
        import inspect

        try:
            # Ibis 6.x
            from ibis.formats.pyarrow import PyArrowType

            to_pyarrow_type = PyArrowType.from_ibis
        except ImportError:
            # Ibis 4.x, 5.x
            from ibis.backends.pyarrow.datatypes import to_pyarrow_type

        if registry is None:
            registry = pc.function_registry()

        def wrapper(ctx, *args):
            out = udf.func(*args, ctx=ctx)
            return out

        in_types = dict(
            zip(
                inspect.getfullargspec(udf.func).args,
                map(to_pyarrow_type, udf.input_type),
            )
        )
        out_type = to_pyarrow_type(udf.output_type)

        if udf.func.__name__ not in set(registry.list_functions()):
            pc.register_scalar_function(
                wrapper,
                udf.func.__name__,
                {
                    "summary": f"UDF {udf.func.__name__} defined in Ibis",
                    "description": "",
                },
                in_types,
                out_type,
            )

    # type-specifications are for ibis' type-checking
    # part of ibis' lazy evaluation
    @elementwise(input_type=["int64"], output_type="int64")
    def add1(col: pa.Int64Scalar, ctx=None) -> pa.Int64Scalar:
        return pc.call_function("add", [col, 1], memory_pool=ctx.memory_pool)

    # @elementwise defines a UDF that operates element-wise
    @elementwise(input_type=["int64"], output_type="int64")
    def sub1(col: pa.Int64Scalar, ctx=None) -> pa.Int64Scalar:
        # PyArrow.compute code
        return pc.call_function("subtract", [col, 1], memory_pool=ctx.memory_pool)

    # registers the UDF on the execution side with PyArrow.
    registry = pc.function_registry()
    register_pyarrow_udf(add1, registry)
    register_pyarrow_udf(sub1, registry)

    # setting up the ibis table
    t = ibis.table([("a", "int")], name="t")
    # the ibis-substrait compiler requires an ibis' table expression
    query = t.mutate(b=add1(t.a), c=sub1(t.a))

    compiler = SubstraitCompiler(
        # UDF uri for the sake of PyArrow
        # so that it knows where to look to find the UDF
        udf_uri="urn:arrow:substrait_simple_extension_function"
    )

    plan = compiler.compile(query)

    arrow_table = pa.Table.from_pydict(
        {
            "a": [1, 2, 3],
        }
    )

    result = run_query(plan, arrow_table)

    assert result[1].to_pylist() == [2, 3, 4]
    assert result[2].to_pylist() == [0, 1, 2]


@arrow12
def test_acero_unsafe_cast(compiler):
    """
    Regression test to catch any behavior change in how Acero handles casting.

    As of arrow 196fbe5f5e0669b1f8bf71005c8a4c6a4e0fb2da, Acero performs an
    unsafe cast where it previously performed a safe cast. The previous behavior
    would cause the following test to throw pyarrow.ArrowInvalid. See
    https://github.com/apache/arrow/issues/34644 for more detail.
    """
    arrow_table = pa.Table.from_pydict(
        {
            "a": [1.8, 2.2, 3.5],
        }
    )
    t = to_ibis_table(arrow_table)
    query = t.mutate(a=t.a.cast("int"))
    plan = compiler.compile(query)
    result = run_query(plan, arrow_table)

    assert result == pa.Table.from_pydict(
        {
            "a": [1, 2, 3],
        }
    )
