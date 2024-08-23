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


all_consumers = ["acero_consumer", "datafusion_consumer"]


@pytest.fixture
def ibis_projection():
    return orders["order_id", "order_total"]


@pytest.fixture
def ibis_mutate():
    return orders.mutate(order_total_plus_1=orders["order_total"] + 1)


@pytest.fixture
def ibis_sort():
    return orders.order_by("order_total")


@pytest.fixture
def ibis_sort_limit():
    return orders.order_by("order_total").limit(2)


@pytest.fixture
def ibis_filter():
    return orders.filter(lambda t: t.order_total > 30)


@pytest.fixture
def ibis_inner_join():
    return orders.join(stores, orders["fk_store_id"] == stores["store_id"])


@pytest.fixture
def ibis_left_join():
    return orders.join(stores, orders["fk_store_id"] == stores["store_id"], how="left")


@pytest.fixture
def ibis_filter_groupby():
    filter_table = orders.join(
        stores, orders["fk_store_id"] == stores["store_id"]
    ).filter(lambda t: t.order_total > 30)

    return filter_table.group_by("city").aggregate(
        sales=filter_table["order_id"].count()
    )


@pytest.fixture
def ibis_filter_groupby_count_distinct():
    filter_table = orders.join(
        stores, orders["fk_store_id"] == stores["store_id"]
    ).filter(lambda t: t.order_total > 30)

    return filter_table.group_by("city").aggregate(sales=filter_table["city"].nunique())


@pytest.fixture
def ibis_aggregate_having():
    return orders.aggregate(
        [orders.order_id.max().name("amax"), orders.order_id.count().name("acount")],
        by="fk_store_id",
        having=(_.order_id.count() > 1),
    )


@pytest.fixture
def ibis_inner_join_chain():
    return orders.join(stores, orders["fk_store_id"] == stores["store_id"]).join(
        customers, orders["fk_customer_id"] == customers["customer_id"]
    )


@pytest.fixture
def ibis_union():
    return orders.union(orders)


@pytest.fixture
def ibis_window():
    return orders.select(
        orders["order_total"].mean().over(ibis.window(group_by="fk_store_id"))
    )


@pytest.fixture
def ibis_is_in():
    return stores.filter(stores.city.isin(["NY", "LA"]))


@pytest.fixture
def ibis_scalar_subquery():
    return orders.filter(orders["order_total"] == orders["order_total"].max())


all_exprs = [
    "ibis_projection",
    "ibis_mutate",
    "ibis_sort",
    "ibis_sort_limit",
    "ibis_filter",
    "ibis_inner_join",
    "ibis_left_join",
    ("ibis_filter_groupby", {"datafusion_consumer": (Exception, "")}),
    (
        "ibis_filter_groupby_count_distinct",
        {
            "acero_consumer": (pa.ArrowNotImplementedError, "Unimplemented"),
            "datafusion_consumer": (Exception, ""),
        },
    ),
    ("ibis_aggregate_having", {"datafusion_consumer": (Exception, "")}),
    "ibis_inner_join_chain",
    "ibis_union",
    ("ibis_window", {"acero_consumer": (pa.ArrowNotImplementedError, "Unimplemented")}),
    "ibis_is_in",
    (
        "ibis_scalar_subquery",
        {"acero_consumer": (pa.ArrowNotImplementedError, "Unimplemented")},
    ),
]


all_fixtures = [
    pytest.param(
        c,
        e[0] if isinstance(e, tuple) else e,
        marks=(
            [pytest.mark.xfail(raises=e[1][c][0], reason=e[1][c][1])]
            if isinstance(e, tuple) and c in e[1]
            else []
        ),
    )
    for e in all_exprs
    for c in all_consumers
]


@pytest.mark.parametrize(("consumer", "expr"), all_fixtures)
def test_parity(consumer: str, expr, request):
    consumer: SubstraitConsumer = request.getfixturevalue(consumer)
    expr = request.getfixturevalue(expr)

    res_duckdb = sort_pyarrow_table(run_query_duckdb(expr, datasets))

    compiler = SubstraitCompiler()

    res_compare = sort_pyarrow_table(consumer.execute(compiler.compile(expr)))

    assert res_compare.equals(res_duckdb)
