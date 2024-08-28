import os
import tempfile

import duckdb
import ibis
import pyarrow as pa
import pyarrow.compute as pc
import pytest
from ibis import _
from ibis.conftest import LINUX, SANDBOXED

from ibis_substrait.compiler.core import SubstraitCompiler

from .parity_utils import (
    AceroSubstraitConsumer,
    DatafusionSubstraitConsumer,
    SubstraitConsumer,
)

nix_linux_sandbox = pytest.mark.xfail(
    LINUX and SANDBOXED,
    reason="nix on linux cannot download duckdb extensions or data due to sandboxing",
    raises=duckdb.IOException,
)


def sort_pyarrow_table(table: pa.Table):
    sort_keys = [(name, "ascending") for name in table.column_names]
    sort_indices = pc.sort_indices(table, sort_keys)
    return pc.take(table, sort_indices)


# TODO move this into a consumer class
def run_query_duckdb(query, datasets):
    with tempfile.TemporaryDirectory() as tempdir:
        con = ibis.duckdb.connect(os.path.join(tempdir, "temp.db"))
        for table_name, pa_table in datasets.items():
            con.create_table(name=table_name, obj=ibis.memtable(pa_table))

        # TODO con.to_pyarrow(query) in duckdb backend doesn't work with latest ibis and pyarrow versions
        res = pa.Table.from_pandas(con.to_pandas(query))
        con.disconnect()
        return res


orders_raw = [
    ("order_id", "int64", [1, 2, 3, 4]),
    ("fk_store_id", "int64", [1, 1, 2, 2]),
    ("fk_customer_id", "int64", [10, 11, 13, 13]),
    ("description", "string", ["A", "B", "C", "D"]),
    ("order_total", "float", [10.0, 32.3, 32.0, 140.0]),
]

stores_raw = [("store_id", "int64", [1, 2, 3]), ("city", "string", ["NY", "LA", "NY"])]

customers_raw = [
    ("customer_id", "int64", [10, 11, 13]),
    ("name", "string", ["Ann", "Bob", "Chris"]),
]

orders = ibis.table([(x[0], x[1]) for x in orders_raw], name="orders")
stores = ibis.table([(x[0], x[1]) for x in stores_raw], name="stores")
customers = ibis.table([(x[0], x[1]) for x in customers_raw], name="customers")

datasets = {
    "orders": pa.Table.from_pydict({x[0]: x[2] for x in orders_raw}),
    "stores": pa.Table.from_pydict({x[0]: x[2] for x in stores_raw}),
    "customers": pa.Table.from_pydict({x[0]: x[2] for x in customers_raw}),
}


@pytest.fixture
def acero_consumer():
    return AceroSubstraitConsumer().with_tables(datasets)


@pytest.fixture
def datafusion_consumer():
    return DatafusionSubstraitConsumer().with_tables(datasets)


def run_parity_test(consumer: SubstraitConsumer, expr):
    res_duckdb = sort_pyarrow_table(run_query_duckdb(expr, datasets))

    compiler = SubstraitCompiler()

    res_compare = sort_pyarrow_table(consumer.execute(compiler.compile(expr)))

    assert res_compare.equals(res_duckdb)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_projection(consumer: str, request):
    expr = orders["order_id", "order_total"]
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_mutate(consumer: str, request):
    expr = orders.mutate(order_total_plus_1=orders["order_total"] + 1)
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_sort(consumer: str, request):
    expr = orders.order_by("order_total")
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_sort_limit(consumer: str, request):
    expr = orders.order_by("order_total").limit(2)
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_filter(consumer: str, request):
    expr = orders.filter(lambda t: t.order_total > 30)
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_inner_join(consumer: str, request):
    expr = orders.join(stores, orders["fk_store_id"] == stores["store_id"])
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize(
    "consumer",
    [
        pytest.param(
            "acero_consumer",
            marks=[
                pytest.mark.xfail(pa.ArrowNotImplementedError, reason="Unimplemented")
            ],
        ),
        "datafusion_consumer",
    ],
)
def test_cross_join(consumer: str, request):
    expr = orders.cross_join(stores)
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_left_join(consumer: str, request):
    expr = orders.join(stores, orders["fk_store_id"] == stores["store_id"], how="left")
    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize(
    "consumer",
    [
        "acero_consumer",
        pytest.param(
            "datafusion_consumer",
            marks=[pytest.mark.xfail(Exception, reason="")],
        ),
    ],
)
def test_filter_groupby(consumer: str, request):
    filter_table = orders.join(
        stores, orders["fk_store_id"] == stores["store_id"]
    ).filter(lambda t: t.order_total > 30)

    expr = filter_table.group_by("city").aggregate(
        sales=filter_table["order_id"].count()
    )

    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize(
    "consumer",
    [
        pytest.param(
            "acero_consumer",
            marks=[
                pytest.mark.xfail(pa.ArrowNotImplementedError, reason="Unimplemented")
            ],
        ),
        pytest.param(
            "datafusion_consumer",
            marks=[pytest.mark.xfail(Exception, reason="")],
        ),
    ],
)
def test_filter_groupby_count_distinct(consumer: str, request):
    filter_table = orders.join(
        stores, orders["fk_store_id"] == stores["store_id"]
    ).filter(lambda t: t.order_total > 30)

    expr = filter_table.group_by("city").aggregate(sales=filter_table["city"].nunique())

    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize(
    "consumer",
    [
        "acero_consumer",
        pytest.param(
            "datafusion_consumer",
            marks=[pytest.mark.xfail(Exception, reason="")],
        ),
    ],
)
def test_aggregate_having(consumer: str, request):
    expr = orders.aggregate(
        [orders.order_id.max().name("amax"), orders.order_id.count().name("acount")],
        by="fk_store_id",
        having=(_.order_id.count() > 1),
    )

    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_inner_join_chain(consumer: str, request):
    expr = orders.join(stores, orders["fk_store_id"] == stores["store_id"]).join(
        customers, orders["fk_customer_id"] == customers["customer_id"]
    )

    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_union(consumer: str, request):
    expr = orders.union(orders)

    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize(
    "consumer",
    [
        pytest.param(
            "acero_consumer",
            marks=[
                pytest.mark.xfail(pa.ArrowNotImplementedError, reason="Unimplemented")
            ],
        ),
        "datafusion_consumer",
    ],
)
def test_window(consumer: str, request):
    expr = orders.select(
        orders["order_total"].mean().over(ibis.window(group_by="fk_store_id"))
    )

    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize("consumer", ["acero_consumer", "datafusion_consumer"])
def test_is_in(consumer: str, request):
    expr = stores.filter(stores.city.isin(["NY", "LA"]))

    run_parity_test(request.getfixturevalue(consumer), expr)


@pytest.mark.parametrize(
    "consumer",
    [
        pytest.param(
            "acero_consumer",
            marks=[
                pytest.mark.xfail(pa.ArrowNotImplementedError, reason="Unimplemented")
            ],
        ),
        "datafusion_consumer",
    ],
)
def test_scalar_subquery(consumer: str, request):
    expr = orders.filter(orders["order_total"] == orders["order_total"].max())

    run_parity_test(request.getfixturevalue(consumer), expr)
