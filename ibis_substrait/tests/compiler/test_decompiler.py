import ibis
import ibis.expr.datatypes as dt
import pytest
from packaging import version

from ibis_substrait.compiler.decompile import decompile, decompile_schema
from ibis_substrait.proto.substrait import type_pb2 as stt


@pytest.fixture
def t():
    return ibis.table(
        [
            (
                "a",
                dt.Array(dt.Struct.from_tuples([("b", "int64"), ("c", "int64")])),
            ),
            (
                "b",
                dt.Array(dt.Struct.from_tuples([("b", "int64"), ("c", "int64")])),
            ),
            ("c", "string"),
            ("d", "int64"),
        ],
        name="t",
    )


@pytest.fixture
def s():
    return ibis.table([("c", "string"), ("d", "int64")], name="s")


@pytest.mark.parametrize(
    "expr_fn",
    [
        pytest.param(lambda t: t, id="read_rel"),
        pytest.param(
            # TODO: ibis: compare .type() instead of dtype on literals
            lambda t: t[t.d == ibis.literal(1, type="int64")],
            id="filter_rel",
        ),
        pytest.param(lambda t: t.limit(5), id="fetch_rel"),
        pytest.param(lambda t: t.sort_by("d"), id="sort_rel_single_key"),
        pytest.param(
            lambda t: t.sort_by(ibis.desc("d")), id="sort_rel_single_key_desc"
        ),
        pytest.param(lambda t: t.sort_by(["c", "d"]), id="sort_rel_double_key"),
        pytest.param(
            lambda t: t.sort_by(["c", ibis.desc("d")]),
            id="sort_rel_double_key_mixed_order",
        ),
        pytest.param(lambda t: t.union(t, distinct=True), id="set_union_distinct"),
    ]
    + [
        pytest.param(lambda t: getattr(t, method)(t), id=f"set_{method}")
        for method in ("union", "difference", "intersect")
    ],
)
def test_decompile(t, compiler, expr_fn):
    expr = expr_fn(t)
    plan = compiler.compile(expr)
    # TODO: only a single relation per plan is supported right now
    (result,) = decompile(plan)
    assert result.equals(expr)


@pytest.mark.parametrize(
    "expr_fn",
    [
        pytest.param(lambda t: t.projection(["b"]), id="project_one"),
        pytest.param(lambda t: t.projection(["b", "d"]), id="project_two"),
    ],
)
def test_decompile_project(t, compiler, expr_fn):
    expr = expr_fn(t)
    plan = compiler.compile(expr)
    (result,) = decompile(plan)
    assert result.equals(expr)


def test_decompile_aggregation_not_grouped(t, compiler):
    # FIXME: names are not preserved
    expr = t.aggregate(sum_d=lambda t: t.d.sum())
    plan = compiler.compile(expr)
    # TODO: only a single relation per plan is supported right now
    (result,) = decompile(plan)
    assert result.equals(expr)


def test_decompile_aggregation_grouped(t, compiler):
    # FIXME: names are not preserved
    expr = t.group_by(["c"]).aggregate(sum_d=lambda t: t.d.sum())
    plan = compiler.compile(expr)
    # TODO: only a single relation per plan is supported right now
    (result,) = decompile(plan)
    assert result.equals(expr)


def test_decompile_schema(t):
    input = stt.NamedStruct(
        names=["a", "b", "c", "b", "b", "c", "c", "d"],
        struct=stt.Type.Struct(
            types=[
                stt.Type(
                    list=stt.Type.List(
                        type=stt.Type(
                            struct=stt.Type.Struct(
                                types=[
                                    stt.Type(i64=stt.Type.I64()),
                                    stt.Type(i64=stt.Type.I64()),
                                ]
                            )
                        )
                    )
                ),
                stt.Type(
                    list=stt.Type.List(
                        type=stt.Type(
                            struct=stt.Type.Struct(
                                types=[
                                    stt.Type(i64=stt.Type.I64()),
                                    stt.Type(i64=stt.Type.I64()),
                                ]
                            )
                        )
                    )
                ),
                stt.Type(string=stt.Type.String()),
                stt.Type(i64=stt.Type.I64()),
            ]
        ),
    )

    expected = t.schema()

    assert decompile_schema(input) == expected


@pytest.mark.parametrize(
    "join_type",
    [
        pytest.param(
            "inner",
            marks=[
                pytest.mark.xfail(
                    version.parse(ibis.__version__) >= version.parse("3.0.0"),
                    reason="roundtrip joins broken on 3.x",
                )
            ],
        ),
        pytest.param(
            "outer",
            marks=[
                pytest.mark.xfail(
                    version.parse(ibis.__version__) >= version.parse("3.0.0"),
                    reason="roundtrip joins broken on 3.x",
                )
            ],
        ),
        pytest.param(
            "left",
            marks=[
                pytest.mark.xfail(
                    version.parse(ibis.__version__) >= version.parse("3.0.0"),
                    reason="roundtrip joins broken on 3.x",
                )
            ],
        ),
        "semi",
        "anti",
    ],
)
def test_decompile_join(t, s, compiler, join_type):
    method = getattr(t, f"{join_type}_join")
    expr = method(s, predicates=["c"])[t.a, t.b, s.d]
    plan = compiler.compile(expr)
    # TODO: only a single relation per plan is supported right now
    (result,) = decompile(plan)
    assert result.equals(expr)


@pytest.mark.skipif(
    version.parse(ibis.__version__) < version.parse("3.0.0"),
    reason="Different failure mode on 2.1.1",
)
@pytest.mark.xfail(
    version.parse(ibis.__version__) >= version.parse("3.0.0"),
    reason="roundtrip joins broken on 3.x",
)
def test_decompile_right_join_ibis3(t, s, compiler):
    expr = t.right_join(s, predicates=["c"])[t.a, t.b, s.d]
    plan = compiler.compile(expr)
    (result,) = decompile(plan)
    assert result.equals(expr)


@pytest.mark.skipif(
    version.parse(ibis.__version__) >= version.parse("3"),
    reason="Different failure mode on 3.x",
)
@pytest.mark.xfail(raises=AttributeError)
def test_decompile_right_join_ibis2(t, s, compiler):
    expr = t.right_join(s, predicates=["c"])[t.a, t.b, s.d]
    plan = compiler.compile(expr)
    (result,) = decompile(plan)
    assert result.equals(expr)
