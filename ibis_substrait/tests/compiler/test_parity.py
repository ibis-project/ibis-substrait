import os
import tempfile

import duckdb
import ibis
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.substrait as pa_substrait
import pytest
from ibis import _
from ibis.conftest import LINUX, SANDBOXED

from ibis_substrait.compiler.core import SubstraitCompiler

nix_linux_sandbox = pytest.mark.xfail(
    LINUX and SANDBOXED,
    reason="nix on linux cannot download duckdb extensions or data due to sandboxing",
    raises=duckdb.IOException,
)


def sort_pyarrow_table(table: pa.Table):
    sort_keys = [(name, "ascending") for name in table.column_names]
    sort_indices = pc.sort_indices(table, sort_keys)
    return pc.take(table, sort_indices)


def run_query_acero(plan, datasets, compiler):
    def get_table_provider(datasets):
        def table_provider(names, schema):
            return datasets[names[0]]

        return table_provider

    plan = compiler.compile(plan)
    query_bytes = plan.SerializeToString()
    result = pa_substrait.run_query(
        # TODO is this still necessary?
        # PyArrow wants its bytes in a very specific byte-string
        pa.py_buffer(query_bytes),
        table_provider=get_table_provider(datasets),
    )

    results = result.read_all()
    assert type(results) == pa.lib.Table

    return results


def run_query_duckdb(query, datasets):
    with tempfile.TemporaryDirectory() as tempdir:
        con = ibis.duckdb.connect(os.path.join(tempdir, "temp.db"))
        for table_name, pa_table in datasets.items():
            con.create_table(name=table_name, obj=ibis.memtable(pa_table))

        # TODO con.to_pyarrow(query) in duckdb backend doesn't work with latest ibis and pyarrow versions
        res = pa.Table.from_pandas(con.to_pandas(query))
        con.disconnect()
        return res


def run_query_duckdb_substrait(expr, datasets, compiler):
    import duckdb

    with tempfile.TemporaryDirectory() as tempdir:
        con = duckdb.connect(database=os.path.join(tempdir, "temp.db"))
        con.sql(f"SET home_directory='{tempdir}'")
        con.install_extension("substrait")
        con.load_extension("substrait")

        for k, v in datasets.items():  # noqa: B007
            con.sql(f"CREATE TABLE {k} AS SELECT * FROM v")

        plan = compiler.compile(expr)
        result = con.from_substrait(plan.SerializeToString())
        return result.fetch_arrow_table()


def run_parity_tests(expr, datasets, compiler, engines=None):
    if engines is None:
        engines = ["acero"]  # duckdb_substrait disabled because can't run on windows
    res_duckdb = sort_pyarrow_table(run_query_duckdb(expr, datasets))
    if "acero" in engines:
        res_acero = sort_pyarrow_table(run_query_acero(expr, datasets, compiler))
        assert res_acero.equals(res_duckdb)

    if "duckdb_substrait" in engines:
        res_duckdb_substrait = sort_pyarrow_table(
            run_query_duckdb_substrait(expr, datasets, compiler)
        )
        assert res_duckdb_substrait.equals(res_duckdb)


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


def test_projection():
    expr = orders["order_id", "order_total"]

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_mutate():
    expr = orders.mutate(order_total_plus_1=orders["order_total"] + 1)

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_sort():
    expr = orders.order_by("order_total")

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_sort_limit():
    expr = orders.order_by("order_total").limit(2)

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_filter():
    filtered_table = orders.filter(lambda t: t.order_total > 30)

    compiler = SubstraitCompiler()
    run_parity_tests(filtered_table, datasets, compiler=compiler)


def test_inner_join():
    expr = orders.join(stores, orders["fk_store_id"] == stores["store_id"])

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_left_join():
    expr = orders.join(stores, orders["fk_store_id"] == stores["store_id"], how="left")

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_filter_groupby():
    filter_table = orders.join(
        stores, orders["fk_store_id"] == stores["store_id"]
    ).filter(lambda t: t.order_total > 30)

    grouped_table = filter_table.group_by("city").aggregate(
        sales=filter_table["order_id"].count()
    )

    compiler = SubstraitCompiler()
    run_parity_tests(grouped_table, datasets, compiler=compiler)


def test_filter_groupby_count_distinct():
    filter_table = orders.join(
        stores, orders["fk_store_id"] == stores["store_id"]
    ).filter(lambda t: t.order_total > 30)

    grouped_table = filter_table.group_by("city").aggregate(
        sales=filter_table["city"].nunique()
    )

    compiler = SubstraitCompiler()
    run_parity_tests(grouped_table, datasets, compiler=compiler, engines=[])


def test_aggregate_having():
    expr = orders.aggregate(
        [orders.order_id.max().name("amax"), orders.order_id.count().name("acount")],
        by="fk_store_id",
        having=(_.order_id.count() > 1),
    )

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_inner_join_chain():
    expr = orders.join(stores, orders["fk_store_id"] == stores["store_id"]).join(
        customers, orders["fk_customer_id"] == customers["customer_id"]
    )

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_union():
    expr = orders.union(orders)

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


# TODO acero doesn't seem to support this, maybe run duckdb on both sides?
def test_window():
    expr = orders.select(
        orders["order_total"].mean().over(ibis.window(group_by="fk_store_id"))
    )

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler, engines=[])


def test_is_in():
    expr = stores.filter(stores.city.isin(["NY", "LA"]))

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler)


def test_scalar_subquery():
    expr = orders.filter(orders["order_total"] == orders["order_total"].max())

    compiler = SubstraitCompiler()
    run_parity_tests(expr, datasets, compiler=compiler, engines=[])
