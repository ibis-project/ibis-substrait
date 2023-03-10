import ibis
import pytest

from ibis_substrait.compiler.core import SubstraitCompiler

compiler = SubstraitCompiler()


def get_table_provider(tbl):
    """Create a table_provider that always returns tbl"""

    def table_provider(names, schema):
        return tbl

    return table_provider


def to_ibis_table(arrow_table, table_name="t1"):
    """Create ibis Table from pyarrow Table"""
    return ibis.table(
        zip(arrow_table.schema.names, [str(type) for type in arrow_table.schema.types]),
        name=table_name,
    )


def run_query(expression, tbl, pa, substrait):
    compiled = compiler.compile(expression)
    query_bytes = compiled.SerializeToString()
    result = substrait.run_query(
        pa.py_buffer(query_bytes), table_provider=get_table_provider(tbl)
    )

    results = result.read_all()
    assert type(results) == pa.lib.Table

    return results


# WIP: I'm not sure how best to parameterize the query too without a ref to the Table
testdata = [
    (
        {
            "a": [1, 2, 3],
            "b": [3.4, 3.7, 2.0],
            "c": ["x", "y", "z"],
            "d": [True, False, True],
        },
        {
            "a": [1, 2, 3],
            "b": [3.4, 3.7, 2.0],
            "c": ["x", "y", "z"],
            "d": [True, False, True],
        },
    )
]


@pytest.mark.parametrize("input,output", testdata)
def test_pyarrow_produces_correct_result(input, output):
    pa = pytest.importorskip("pyarrow")
    substrait = pytest.importorskip("pyarrow.substrait")

    arrow_table = pa.Table.from_pydict(input)
    ibis_table = to_ibis_table(arrow_table)
    query = ibis_table # identity
    result = run_query(query, arrow_table, pa, substrait)

    assert result == arrow_table


def test_pyarrow_can_consume_basic_operations():
    pa = pytest.importorskip("pyarrow")
    substrait = pytest.importorskip("pyarrow.substrait")

    arrow_table = pa.Table.from_pydict(
        {
            "a": [1, 2, 3],
            "b": [3.4, 3.7, 2.0],
            "c": ["x", "y", "z"],
            "d": [True, False, True],
        }
    )

    t = to_ibis_table(arrow_table)

    # identity
    query = t
    result = run_query(query, arrow_table, pa, substrait)
    assert result == arrow_table

    # mutate, re-use column
    query = t.mutate(a=t.a * 2)
    result = run_query(query, arrow_table, pa, substrait)

    assert set(result.column_names) == set(arrow_table.column_names)

    # mutate, add new derived column
    query = t.mutate(e=t.b + 1)
    result = run_query(query, arrow_table, pa, substrait)

    assert set(result.column_names) == {*arrow_table.column_names, "e"}
