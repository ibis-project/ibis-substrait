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


@pytest.fixture
def orders():
    return ibis.table(
        [
            ("o_orderkey", dt.int32(nullable=False)),
            ("o_custkey", dt.int32(nullable=False)),
            ("o_orderstatus", dt.string(nullable=False)),
            ("o_totalprice", dt.Decimal(precision=15, scale=2, nullable=False)),
            ("o_orderdate", dt.date(nullable=False)),
            ("o_orderpriority", dt.string(nullable=False)),
            ("o_clerk", dt.string(nullable=False)),
            ("o_shippriority", dt.int32(nullable=False)),
            ("o_comment", dt.string(nullable=False)),
        ],
        name="orders",
    )


@pytest.fixture
def partsupp():
    return ibis.table(
        [
            ("ps_partkey", dt.int32(nullable=False)),
            ("ps_suppkey", dt.int32(nullable=False)),
            ("ps_availqty", dt.int32(nullable=False)),
            ("ps_supplycost", dt.Decimal(precision=15, scale=2, nullable=False)),
            ("ps_comment", dt.string(nullable=False)),
        ],
        name="partsupp",
    )


@pytest.fixture
def part():
    return ibis.table(
        [
            ("p_partkey", dt.int32(nullable=False)),
            ("p_name", dt.string(nullable=False)),
            ("p_mfgr", dt.string(nullable=False)),
            ("p_brand", dt.string(nullable=False)),
            ("p_type", dt.string(nullable=False)),
            ("p_size", dt.int32(nullable=False)),
            ("p_container", dt.string(nullable=False)),
            ("p_retailprice", dt.Decimal(precision=15, scale=2, nullable=False)),
            ("p_comment", dt.string(nullable=False)),
        ],
        name="part",
    )


@pytest.fixture
def customer():
    return ibis.table(
        [
            ("c_custkey", dt.int32(nullable=False)),
            ("c_name", dt.string(nullable=False)),
            ("c_address", dt.string(nullable=False)),
            ("c_nationkey", dt.int32(nullable=False)),
            ("c_phone", dt.string(nullable=False)),
            ("c_acctbal", dt.Decimal(precision=15, scale=2, nullable=False)),
            ("c_mktsegment", dt.string(nullable=False)),
            ("c_comment", dt.string(nullable=False)),
        ],
        name="customer",
    )


@pytest.fixture
def supplier():
    return ibis.table(
        [
            ("s_suppkey", dt.int32(nullable=False)),
            ("s_name", dt.string(nullable=False)),
            ("s_address", dt.string(nullable=False)),
            ("s_nationkey", dt.int32(nullable=False)),
            ("s_phone", dt.string(nullable=False)),
            ("s_acctbal", dt.Decimal(precision=15, scale=2, nullable=False)),
            ("s_comment", dt.string(nullable=False)),
        ],
        name="supplier",
    )


@pytest.fixture
def nation():
    return ibis.table(
        [
            ("n_nationkey", dt.int32(nullable=False)),
            ("n_name", dt.string(nullable=False)),
            ("n_regionkey", dt.int32(nullable=False)),
            ("n_comment", dt.string(nullable=False)),
        ],
        name="nation",
    )


@pytest.fixture
def region():
    return ibis.table(
        [
            ("r_regionkey", dt.int32(nullable=False)),
            ("r_name", dt.string(nullable=False)),
            ("r_comment", dt.string(nullable=False)),
        ],
        name="region",
    )
