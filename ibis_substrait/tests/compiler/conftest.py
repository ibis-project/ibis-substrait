import ibis
import ibis.expr.datatypes as dt
import pytest


def pytest_runtest_setup(item):
    if item.function.__name__ == "test_decompile" and any(
        item.iter_markers(name="no_decompile")
    ):
        item.add_marker(
            pytest.mark.xfail(
                raises=(AssertionError, NotImplementedError),
                reason=f"`{item.callspec.id}` cannot yet be reified",
            )
        )


@pytest.fixture
def lineitem():
    return ibis.table(
        [
            ("l_orderkey", dt.int64),
            ("l_partkey", dt.int64),
            ("l_suppkey", dt.int64),
            ("l_linenumber", dt.int64),
            ("l_quantity", dt.Decimal(15, 2)),
            ("l_extendedprice", dt.Decimal(15, 2)),
            ("l_discount", dt.Decimal(15, 2)),
            ("l_tax", dt.Decimal(15, 2)),
            ("l_returnflag", dt.string),
            ("l_linestatus", dt.string),
            ("l_shipdate", dt.date),
            ("l_commitdate", dt.date),
            ("l_receiptdate", dt.date),
            ("l_shipinstruct", dt.string),
            ("l_shipmode", dt.string),
            ("l_comment", dt.string),
        ],
        name="lineitem",
    )
