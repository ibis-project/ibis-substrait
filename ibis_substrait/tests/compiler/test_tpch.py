from datetime import date

import ibis
import pytest
from pytest_lazyfixture import lazy_fixture
from substrait_validator import Config, check_plan

from ibis_substrait.compiler.decompile import decompile


@pytest.fixture
def tpc_h01(lineitem):
    return (
        lineitem.filter(lambda t: t.l_shipdate <= date(year=1998, month=9, day=2))
        .group_by(["l_returnflag", "l_linestatus"])
        .aggregate(
            sum_qty=lambda t: t.l_quantity.sum(),
            sum_base_price=lambda t: t.l_extendedprice.sum(),
            sum_disc_price=lambda t: (t.l_extendedprice * (1 - t.l_discount)).sum(),
            sum_charge=lambda t: (
                t.l_extendedprice * (1 - t.l_discount) * (1 + t.l_tax)
            ).sum(),
            avg_qty=lambda t: t.l_quantity.mean(),
            avg_price=lambda t: t.l_extendedprice.mean(),
            avg_disc=lambda t: t.l_discount.mean(),
            count_order=lambda t: t.count(),
        )
        .sort_by(["l_returnflag", "l_linestatus"])
    )


@pytest.fixture
def tpc_h02(
    part, supplier, partsupp, nation, region, REGION="EUROPE", SIZE=25, TYPE="BRASS"
):
    "Minimum Cost Supplier Query (Q2)"

    expr = (
        part.join(partsupp, part.p_partkey == partsupp.ps_partkey)
        .join(supplier, supplier.s_suppkey == partsupp.ps_suppkey)
        .join(nation, supplier.s_nationkey == nation.n_nationkey)
        .join(region, nation.n_regionkey == region.r_regionkey)
    )

    subexpr = (
        partsupp.join(supplier, supplier.s_suppkey == partsupp.ps_suppkey)
        .join(nation, supplier.s_nationkey == nation.n_nationkey)
        .join(region, nation.n_regionkey == region.r_regionkey)
    )

    subexpr = subexpr[
        (subexpr.r_name == REGION) & (expr.p_partkey == subexpr.ps_partkey)
    ]

    filters = [
        expr.p_size == SIZE,
        expr.p_type.like("%" + TYPE),
        expr.r_name == REGION,
        expr.ps_supplycost == subexpr.ps_supplycost.min(),
    ]
    q = expr.filter(filters)

    q = q.select(
        [
            q.s_acctbal,
            q.s_name,
            q.n_name,
            q.p_partkey,
            q.p_mfgr,
            q.s_address,
            q.s_phone,
            q.s_comment,
        ]
    )

    return q.sort_by(
        [
            ibis.desc(q.s_acctbal),
            q.n_name,
            q.s_name,
            q.p_partkey,
        ]
    ).limit(100)


@pytest.fixture
def tpc_h03(
    customer,
    orders,
    lineitem,
):
    DATE = "1995-03-15"
    q = customer.join(orders, customer.c_custkey == orders.o_custkey)
    q = q.join(lineitem, lineitem.l_orderkey == orders.o_orderkey)
    q = q.filter(
        [q.c_mktsegment == "BUILDING", q.o_orderdate < DATE, q.l_shipdate > DATE]
    )
    qg = q.group_by([q.l_orderkey, q.o_orderdate, q.o_shippriority])
    q = qg.aggregate(revenue=(q.l_extendedprice * (1 - q.l_discount)).sum())
    q = q.sort_by([ibis.desc(q.revenue), q.o_orderdate])
    q = q.limit(10)

    return q


@pytest.fixture
def tpc_h04(orders, lineitem):
    cond = (lineitem.l_orderkey == orders.o_orderkey) & (
        lineitem.l_commitdate < lineitem.l_receiptdate
    )
    q = orders.filter(
        [
            cond.any(),
            orders.o_orderdate >= "1993-07-01",
            orders.o_orderdate < "1993-10-01",
        ]
    )
    q = q.group_by([orders.o_orderpriority])
    q = q.aggregate(order_count=orders.count())
    q = q.sort_by([orders.o_orderpriority])
    return q


@pytest.fixture
def tpc_h05(customer, orders, lineitem, supplier, nation, region):
    q = customer
    q = q.join(orders, customer.c_custkey == orders.o_custkey)
    q = q.join(lineitem, lineitem.l_orderkey == orders.o_orderkey)
    q = q.join(supplier, lineitem.l_suppkey == supplier.s_suppkey)
    q = q.join(
        nation,
        (customer.c_nationkey == supplier.s_nationkey)
        & (supplier.s_nationkey == nation.n_nationkey),
    )
    q = q.join(region, nation.n_regionkey == region.r_regionkey)

    q = q.filter(
        [
            q.r_name == "ASIA",
            q.o_orderdate >= "1994-01-01",
            q.o_orderdate < "1995-01-01",
        ]
    )
    revexpr = q.l_extendedprice * (1 - q.l_discount)
    gq = q.group_by([q.n_name])
    q = gq.aggregate(revenue=revexpr.sum())
    q = q.sort_by([ibis.desc(q.revenue)])
    return q


@pytest.fixture
def tpc_h06(lineitem):
    q = lineitem
    discount_min = round(0.06 - 0.01, 2)
    discount_max = round(0.06 + 0.01, 2)
    q = q.filter(
        [
            q.l_shipdate >= "1994-01-01",
            q.l_shipdate < "1995-01-01",
            q.l_discount.between(discount_min, discount_max),
            q.l_quantity < 24,
        ]
    )
    q = q.aggregate(revenue=(q.l_extendedprice * q.l_discount).sum())
    return q


@pytest.fixture
def tpc_h07(supplier, lineitem, orders, customer, nation):
    q = supplier
    q = q.join(lineitem, supplier.s_suppkey == lineitem.l_suppkey)
    q = q.join(orders, orders.o_orderkey == lineitem.l_orderkey)
    q = q.join(customer, customer.c_custkey == orders.o_custkey)
    n1 = nation
    n2 = nation.view()
    q = q.join(n1, supplier.s_nationkey == n1.n_nationkey)
    q = q.join(n2, customer.c_nationkey == n2.n_nationkey)

    q = q[
        n1.n_name.name("supp_nation"),
        n2.n_name.name("cust_nation"),
        lineitem.l_shipdate,
        lineitem.l_extendedprice,
        lineitem.l_discount,
        lineitem.l_shipdate.year().cast("string").name("l_year"),
        (lineitem.l_extendedprice * (1 - lineitem.l_discount)).name("volume"),
    ]

    q = q.filter(
        [
            ((q.cust_nation == "FRANCE") & (q.supp_nation == "GERMANY"))
            | ((q.cust_nation == "GERMANY") & (q.supp_nation == "FRANCE")),
            q.l_shipdate.between("1995-01-01", "1996-12-31"),
        ]
    )

    gq = q.group_by(["supp_nation", "cust_nation", "l_year"])
    q = gq.aggregate(revenue=q.volume.sum())
    q = q.sort_by(["supp_nation", "cust_nation", "l_year"])

    return q


@pytest.fixture
def tpc_h08(
    part,
    supplier,
    lineitem,
    orders,
    customer,
    region,
    nation,
):
    n1 = nation
    n2 = n1.view()

    q = part
    q = q.join(lineitem, part.p_partkey == lineitem.l_partkey)
    q = q.join(supplier, supplier.s_suppkey == lineitem.l_suppkey)
    q = q.join(orders, lineitem.l_orderkey == orders.o_orderkey)
    q = q.join(customer, orders.o_custkey == customer.c_custkey)
    q = q.join(n1, customer.c_nationkey == n1.n_nationkey)
    q = q.join(region, n1.n_regionkey == region.r_regionkey)
    q = q.join(n2, supplier.s_nationkey == n2.n_nationkey)

    q = q[
        orders.o_orderdate.year().cast("string").name("o_year"),
        (lineitem.l_extendedprice * (1 - lineitem.l_discount)).name("volume"),
        n2.n_name.name("nation"),
        region.r_name,
        orders.o_orderdate,
        part.p_type,
    ]

    q = q.filter(
        [
            q.r_name == "AMERICA",
            q.o_orderdate.between("1995-01-01", "1996-12-31"),
            q.p_type == "ECONOMY ANODIZED STEEL",
        ]
    )

    q = q.mutate(
        nation_volume=ibis.case().when(q.nation == "BRAZIL", q.volume).else_(0).end()
    )
    gq = q.group_by([q.o_year])
    q = gq.aggregate(mkt_share=q.nation_volume.sum() / q.volume.sum())
    q = q.sort_by([q.o_year])
    return q


@pytest.fixture
def tpc_h09(part, supplier, lineitem, partsupp, orders, nation):
    q = lineitem
    q = q.join(supplier, supplier.s_suppkey == lineitem.l_suppkey)
    q = q.join(
        partsupp,
        (partsupp.ps_suppkey == lineitem.l_suppkey)
        & (partsupp.ps_partkey == lineitem.l_partkey),
    )
    q = q.join(part, part.p_partkey == lineitem.l_partkey)
    q = q.join(orders, orders.o_orderkey == lineitem.l_orderkey)
    q = q.join(nation, supplier.s_nationkey == nation.n_nationkey)

    q = q[
        (q.l_extendedprice * (1 - q.l_discount) - q.ps_supplycost * q.l_quantity).name(
            "amount"
        ),
        q.o_orderdate.year().cast("string").name("o_year"),
        q.n_name.name("nation"),
        q.p_name,
    ]

    q = q.filter([q.p_name.like("%GREEN%")])

    gq = q.group_by([q.nation, q.o_year])
    q = gq.aggregate(sum_profit=q.amount.sum())
    q = q.sort_by([q.nation, ibis.desc(q.o_year)])
    return q


@pytest.fixture
def tpc_h10(customer, orders, lineitem, nation):
    q = customer
    q = q.join(orders, customer.c_custkey == orders.o_custkey)
    q = q.join(lineitem, lineitem.l_orderkey == orders.o_orderkey)
    q = q.join(nation, customer.c_nationkey == nation.n_nationkey)

    q = q.filter(
        [
            (q.o_orderdate >= "1993-01-01") & (q.o_orderdate < "1993-04-01"),
            q.l_returnflag == "R",
        ]
    )

    gq = q.group_by(
        [
            q.c_custkey,
            q.c_name,
            q.c_acctbal,
            q.c_phone,
            q.n_name,
            q.c_address,
            q.c_comment,
        ]
    )
    q = gq.aggregate(revenue=(q.l_extendedprice * (1 - q.l_discount)).sum())

    q = q.sort_by(ibis.desc(q.revenue))
    return q.limit(20)


@pytest.fixture
def tpc_h11(partsupp, supplier, nation):
    q = partsupp
    q = q.join(supplier, partsupp.ps_suppkey == supplier.s_suppkey)
    q = q.join(nation, nation.n_nationkey == supplier.s_nationkey)

    q = q.filter([q.n_name == "GERMANY"])

    innerq = partsupp
    innerq = innerq.join(supplier, partsupp.ps_suppkey == supplier.s_suppkey)
    innerq = innerq.join(nation, nation.n_nationkey == supplier.s_nationkey)
    innerq = innerq.filter([innerq.n_name == "GERMANY"])
    innerq = innerq.aggregate(total=(innerq.ps_supplycost * innerq.ps_availqty).sum())

    gq = q.group_by([q.ps_partkey])
    q = gq.aggregate(value=(q.ps_supplycost * q.ps_availqty).sum())
    q = q.filter([q.value > innerq.total * 0.0001])
    q = q.sort_by(ibis.desc(q.value))
    return q


@pytest.fixture
def tpc_h12(orders, lineitem):
    q = orders
    q = q.join(lineitem, orders.o_orderkey == lineitem.l_orderkey)

    q = q.filter(
        [
            q.l_shipmode.isin(["MAIL", "SHIP"]),
            q.l_commitdate < q.l_receiptdate,
            q.l_shipdate < q.l_commitdate,
            q.l_receiptdate >= "1994-01-01",
            q.l_receiptdate < "1995-01-01",
        ]
    )

    gq = q.group_by([q.l_shipmode])
    q = gq.aggregate(
        high_line_count=(
            q.o_orderpriority.case()
            .when("1-URGENT", 1)
            .when("2-HIGH", 1)
            .else_(0)
            .end()
        ).sum(),
        low_line_count=(
            q.o_orderpriority.case()
            .when("1-URGENT", 0)
            .when("2-HIGH", 0)
            .else_(1)
            .end()
        ).sum(),
    )
    q = q.sort_by(q.l_shipmode)

    return q


@pytest.fixture
def tpc_h13(customer, orders):
    innerq = customer
    innerq = innerq.left_join(
        orders,
        (customer.c_custkey == orders.o_custkey)
        & ~orders.o_comment.like("%special%requests%"),
    )
    innergq = innerq.group_by([innerq.c_custkey])
    innerq = innergq.aggregate(c_count=innerq.o_orderkey.count())

    gq = innerq.group_by([innerq.c_count])
    q = gq.aggregate(custdist=innerq.count())

    q = q.sort_by([ibis.desc(q.custdist), ibis.desc(q.c_count)])
    return q


@pytest.fixture
def tpc_h14(lineitem, part):
    q = lineitem
    q = q.join(part, lineitem.l_partkey == part.p_partkey)
    q = q.filter([q.l_shipdate >= "1995-09-01", q.l_shipdate < "1995-10-01"])

    revenue = q.l_extendedprice * (1 - q.l_discount)
    promo_revenue = q.p_type.like("PROMO%").ifelse(revenue, 0)

    q = q.aggregate(promo_revenue=100 * promo_revenue.sum() / revenue.sum())
    return q


@pytest.fixture
def tpc_h15(lineitem, supplier):
    qrev = lineitem
    qrev = qrev.filter(
        [lineitem.l_shipdate >= "1996-01-01", lineitem.l_shipdate < "1996-04-01"]
    )

    gqrev = qrev.group_by([lineitem.l_suppkey])
    qrev = gqrev.aggregate(
        total_revenue=(qrev.l_extendedprice * (1 - qrev.l_discount)).sum()
    )

    q = supplier.join(qrev, supplier.s_suppkey == qrev.l_suppkey)
    q = q.filter([q.total_revenue == qrev.total_revenue.max()])
    q = q.sort_by([q.s_suppkey])
    q = q[q.s_suppkey, q.s_name, q.s_address, q.s_phone, q.total_revenue]
    return q


@pytest.fixture
def tpc_h16(partsupp, part, supplier):
    q = partsupp.join(part, part.p_partkey == partsupp.ps_partkey)
    q = q.filter(
        [
            q.p_brand != "Brand#45",
            ~q.p_type.like("MEDIUM POLISHED%"),
            q.p_size.isin((49, 14, 23, 45, 19, 3, 36, 9)),
            ~q.ps_suppkey.isin(
                supplier.filter(
                    [supplier.s_comment.like("%Customer%Complaints%")]
                ).s_suppkey
            ),
        ]
    )
    gq = q.groupby([q.p_brand, q.p_type, q.p_size])
    q = gq.aggregate(supplier_cnt=q.ps_suppkey.nunique())
    q = q.sort_by([ibis.desc(q.supplier_cnt), q.p_brand, q.p_type, q.p_size])
    return q


@pytest.fixture
def tpc_h17(lineitem, part):
    q = lineitem.join(part, part.p_partkey == lineitem.l_partkey)

    innerq = lineitem
    innerq = innerq.filter([innerq.l_partkey == q.p_partkey])

    q = q.filter(
        [
            q.p_brand == "Brand#23",
            q.p_container == "MED BOX",
            q.l_quantity < (0.2 * innerq.l_quantity.mean()),
        ]
    )
    q = q.aggregate(avg_yearly=q.l_extendedprice.sum() / 7.0)
    return q


@pytest.fixture
def tpc_h18(customer, orders, lineitem):
    subgq = lineitem.groupby([lineitem.l_orderkey])
    subq = subgq.aggregate(qty_sum=lineitem.l_quantity.sum())
    subq = subq.filter([subq.qty_sum > 300])

    q = customer
    q = q.join(orders, customer.c_custkey == orders.o_custkey)
    q = q.join(lineitem, orders.o_orderkey == lineitem.l_orderkey)
    q = q.filter([q.o_orderkey.isin(subq.l_orderkey)])

    gq = q.groupby([q.c_name, q.c_custkey, q.o_orderkey, q.o_orderdate, q.o_totalprice])
    q = gq.aggregate(sum_qty=q.l_quantity.sum())
    q = q.sort_by([ibis.desc(q.o_totalprice), q.o_orderdate])
    return q.limit(100)


@pytest.fixture
def tpc_h19(lineitem, part):
    q = lineitem.join(part, part.p_partkey == lineitem.l_partkey)

    q1 = (
        (q.p_brand == "Brand#12")
        & (q.p_container.isin(("SM CASE", "SM BOX", "SM PACK", "SM PKG")))
        & (q.l_quantity >= 1)
        & (q.l_quantity <= 1 + 10)
        & (q.p_size.between(1, 5))
        & (q.l_shipmode.isin(("AIR", "AIR REG")))
        & (q.l_shipinstruct == "DELIVER IN PERSON")
    )

    q2 = (
        (q.p_brand == "Brand#23")
        & (q.p_container.isin(("MED BAG", "MED BOX", "MED PKG", "MED PACK")))
        & (q.l_quantity >= 10)
        & (q.l_quantity <= 10 + 10)
        & (q.p_size.between(1, 10))
        & (q.l_shipmode.isin(("AIR", "AIR REG")))
        & (q.l_shipinstruct == "DELIVER IN PERSON")
    )

    q3 = (
        (q.p_brand == "Brand#34")
        & (q.p_container.isin(("LG CASE", "LG BOX", "LG PACK", "LG PKG")))
        & (q.l_quantity >= 20)
        & (q.l_quantity <= 20 + 10)
        & (q.p_size.between(1, 15))
        & (q.l_shipmode.isin(("AIR", "AIR REG")))
        & (q.l_shipinstruct == "DELIVER IN PERSON")
    )

    q = q.filter([q1 | q2 | q3])
    q = q.aggregate(revenue=(q.l_extendedprice * (1 - q.l_discount)).sum())
    return q


@pytest.fixture
def tpc_h20(supplier, nation, partsupp, part, lineitem):
    q1 = supplier.join(nation, supplier.s_nationkey == nation.n_nationkey)

    q3 = part.filter([part.p_name.like("forest%")])
    q2 = partsupp

    q4 = lineitem.filter(
        [
            lineitem.l_partkey == q2.ps_partkey,
            lineitem.l_suppkey == q2.ps_suppkey,
            lineitem.l_shipdate >= "1994-01-01",
            lineitem.l_shipdate < "1995-01-01",
        ]
    )

    q2 = q2.filter(
        [
            partsupp.ps_partkey.isin(q3.p_partkey),
            partsupp.ps_availqty > 0.5 * q4.l_quantity.sum(),
        ]
    )

    q1 = q1.filter([q1.n_name == "CANADA", q1.s_suppkey.isin(q2.ps_suppkey)])

    q1 = q1[q1.s_name, q1.s_address]

    return q1.sort_by(q1.s_name)


@pytest.fixture
def tpc_h21(supplier, lineitem, orders, nation):
    L2 = lineitem.view()
    L3 = lineitem.view()

    q = supplier
    q = q.join(lineitem, supplier.s_suppkey == lineitem.l_suppkey)
    q = q.join(orders, orders.o_orderkey == lineitem.l_orderkey)
    q = q.join(nation, supplier.s_nationkey == nation.n_nationkey)
    q = q[
        q.l_orderkey.name("l1_orderkey"),
        q.o_orderstatus,
        q.l_receiptdate,
        q.l_commitdate,
        q.l_suppkey.name("l1_suppkey"),
        q.s_name,
        q.n_name,
    ]
    q = q.filter(
        [
            q.o_orderstatus == "F",
            q.l_receiptdate > q.l_commitdate,
            q.n_name == "SAUDI ARABIA",
            ((L2.l_orderkey == q.l1_orderkey) & (L2.l_suppkey != q.l1_suppkey)).any(),
            ~(
                (
                    (L3.l_orderkey == q.l1_orderkey)
                    & (L3.l_suppkey != q.l1_suppkey)
                    & (L3.l_receiptdate > L3.l_commitdate)
                ).any()
            ),
        ]
    )

    gq = q.group_by([q.s_name])
    q = gq.aggregate(numwait=q.count())
    q = q.sort_by([ibis.desc(q.numwait), q.s_name])
    return q.limit(100)


@pytest.fixture
def tpc_h22(customer, orders):
    q = customer.filter(
        [
            customer.c_acctbal > 0.00,
            customer.c_phone.substr(0, 2).isin(
                ("13", "31", "23", "29", "30", "18", "17")
            ),
        ]
    )
    q = q.aggregate(avg_bal=customer.c_acctbal.mean())

    custsale = customer.filter(
        [
            customer.c_phone.substr(0, 2).isin(
                ("13", "31", "23", "29", "30", "18", "17")
            ),
            customer.c_acctbal > q.avg_bal,
            ~(orders.o_custkey == customer.c_custkey).any(),
        ]
    )
    custsale = custsale[
        customer.c_phone.substr(0, 2).name("cntrycode"), customer.c_acctbal
    ]

    gq = custsale.group_by(custsale.cntrycode)
    outerq = gq.aggregate(numcust=custsale.count(), totacctbal=custsale.c_acctbal.sum())

    return outerq.sort_by(outerq.cntrycode)


def test_tpch1(tpc_h01, lineitem, compiler):
    plan = compiler.compile(tpc_h01)
    assert plan.SerializeToString()

    (result,) = decompile(plan)
    expected = (
        lineitem.filter(lambda t: t.l_shipdate <= date(year=1998, month=9, day=2))
        .group_by(["l_returnflag", "l_linestatus"])
        .aggregate(
            sum_qty=lambda t: t.l_quantity.sum(),
            sum_base_price=lambda t: t.l_extendedprice.sum(),
            sum_disc_price=lambda t: (t.l_extendedprice * (1 - t.l_discount)).sum(),
            sum_charge=lambda t: (
                t.l_extendedprice * (1 - t.l_discount) * (1 + t.l_tax)
            ).sum(),
            avg_qty=lambda t: t.l_quantity.mean(),
            avg_price=lambda t: t.l_extendedprice.mean(),
            avg_disc=lambda t: t.l_discount.mean(),
            count_order=lambda t: t.count(),
        )
        .sort_by(["l_returnflag", "l_linestatus"])
    )
    assert result.equals(expected)


TPC_H = [
    lazy_fixture("tpc_h01"),
    pytest.param(
        lazy_fixture("tpc_h02"),
        marks=pytest.mark.xfail(
            raises=AssertionError, reason="Correlated Subquery issues"
        ),
    ),
    lazy_fixture("tpc_h03"),
    lazy_fixture("tpc_h04"),
    lazy_fixture("tpc_h05"),
    lazy_fixture("tpc_h06"),
    lazy_fixture("tpc_h07"),
    pytest.param(
        lazy_fixture("tpc_h08"),
        marks=pytest.mark.xfail(
            raises=TypeError,
            reason="Aggregates need to be handled differently than they are",
        ),
    ),
    lazy_fixture("tpc_h09"),
    lazy_fixture("tpc_h10"),
    lazy_fixture("tpc_h11"),
    lazy_fixture("tpc_h12"),
    lazy_fixture("tpc_h13"),
    pytest.param(
        lazy_fixture("tpc_h14"),
        marks=pytest.mark.xfail(
            raises=TypeError,
            reason="protobuf error resulting subquery (cannot merge Expression and AggregateFunction)",
        ),
    ),
    pytest.param(
        lazy_fixture("tpc_h15"),
        marks=pytest.mark.xfail(
            raises=AssertionError, reason="Correlated Subquery issues"
        ),
    ),
    lazy_fixture("tpc_h16"),
    pytest.param(
        lazy_fixture("tpc_h17"),
        marks=pytest.mark.xfail(
            raises=NotImplementedError,
            reason="ibis.expr.operations.relations.Aggregation",
        ),
    ),
    lazy_fixture("tpc_h18"),
    lazy_fixture("tpc_h19"),
    lazy_fixture("tpc_h20"),
    lazy_fixture("tpc_h21"),
    lazy_fixture("tpc_h22"),
]


@pytest.mark.parametrize(
    "query",
    TPC_H,
)
def test_compile(query, compiler):
    _ = compiler.compile(query)


@pytest.mark.parametrize(
    "query",
    TPC_H,
)
def test_compile_validate(query, compiler):
    plan = compiler.compile(query)

    c = Config()
    # too few field names
    c.override_diagnostic_level(4003, "error", "info")
    # function def unavailable, cannot check validity of call
    c.override_diagnostic_level(6003, "warning", "info")
    # failed to resolve YAML: unknown url type
    c.override_diagnostic_level(2002, "warning", "info")  # too few field names
    # typecast validation rules are net yet implemented
    c.override_diagnostic_level(1, "warning", "info")  # too few field names

    # check_plan takes substrait Plans as arguments but because of namespacing,
    # our plan is no longer strictly a substrait.plan_pb2.Plan.
    # Workaround for now is to send in the bytes which it handles without issue.
    assert check_plan(plan.SerializeToString(), config=c)
