from collections import OrderedDict

import ibis
import ibis.expr.datatypes as dt
import pytest
from google.protobuf import json_format
from ibis import _
from substrait.gen.proto import algebra_pb2 as stalg
from substrait.gen.proto import type_pb2 as stt

from ibis_substrait.compiler.translate import translate

NULLABILITY_NULLABLE = stt.Type.Nullability.NULLABILITY_NULLABLE
NULLABILITY_REQUIRED = stt.Type.Nullability.NULLABILITY_REQUIRED


@pytest.fixture
def t():
    return ibis.table(
        [
            ("full_name", "string"),
            ("age", "int64"),
            ("ts", "timestamp('UTC')"),
            ("delta", "interval"),
        ]
    )


def to_dict(message):
    return json_format.MessageToDict(message)


def test_aggregation(t, compiler):
    expr = (
        t.group_by(name_len=lambda t: t.full_name.length())
        .aggregate(max_age=t.age.max(), min_age=t.age.min())
        .filter(lambda t: t.name_len > 3)
    )
    result = translate(expr, compiler=compiler)
    js = to_dict(result)
    assert js


def test_aggregation_with_sort(t, compiler):
    expr = (
        t.group_by(name_len=lambda t: t.full_name.length())
        .aggregate(max_age=t.age.max(), min_age=t.age.min())
        .order_by(_.max_age)
        .filter(lambda t: t.name_len > 3)
    )
    result = translate(expr, compiler=compiler)
    js = to_dict(result)
    assert js


def test_aggregation_no_args(t, compiler):
    expr = t.group_by("age").count()
    result = translate(expr, compiler=compiler)
    js = to_dict(result)
    assert js


@pytest.mark.parametrize(
    "preceding, following",
    [
        ((4, 2), None),
        (None, (1, 5)),
        (None, None),
        (2, 4),
    ],
)
def test_aggregation_window(t, compiler, preceding, following):
    expr = t.projection(
        [
            t.full_name.length()
            .mean()
            .over(ibis.window(preceding=preceding, following=following, group_by="age"))
        ]
    )
    result = translate(expr, compiler=compiler)
    js = to_dict(result)
    assert js


def test_array_literal(compiler):
    expr = ibis.literal(["a", "b"])
    result = translate(expr, compiler=compiler)
    js = to_dict(result)
    assert js


def test_map_literal(compiler):
    expr = ibis.literal(dict(a=[], b=[2]))
    result = translate(expr, compiler=compiler)
    js = to_dict(result)
    assert js


def test_struct_literal(compiler):
    expr = ibis.literal(OrderedDict(a=1, b=[2.0]))
    result = translate(expr, compiler=compiler)
    js = to_dict(result)
    assert js


def test_translate_table_expansion(compiler):
    t = ibis.table([("a", "int32"), ("b", "int64")], name="table0")
    expr = t.mutate(c=t.a + t.b)
    result = translate(expr, compiler=compiler)
    expected = {
        "project": {
            "common": {"emit": {"outputMapping": [2, 3, 4]}},
            "input": {
                "read": {
                    "common": {"direct": {}},
                    "baseSchema": {
                        "names": ["a", "b"],
                        "struct": {
                            "nullability": "NULLABILITY_REQUIRED",
                            "types": [
                                {"i32": {"nullability": "NULLABILITY_NULLABLE"}},
                                {"i64": {"nullability": "NULLABILITY_NULLABLE"}},
                            ],
                        },
                    },
                    "namedTable": {"names": ["table0"]},
                }
            },
            "expressions": [
                {
                    "selection": {
                        "directReference": {"structField": {}},
                        "rootReference": {},
                    }
                },
                {
                    "selection": {
                        "directReference": {"structField": {"field": 1}},
                        "rootReference": {},
                    }
                },
                {
                    "scalarFunction": {
                        "functionReference": 1,
                        "arguments": [
                            {
                                "value": {
                                    "cast": {
                                        "failureBehavior": "FAILURE_BEHAVIOR_THROW_EXCEPTION",
                                        "input": {
                                            "selection": {
                                                "directReference": {"structField": {}},
                                                "rootReference": {},
                                            },
                                        },
                                        "type": {
                                            "i64": {
                                                "nullability": "NULLABILITY_NULLABLE"
                                            }
                                        },
                                    },
                                },
                            },
                            {
                                "value": {
                                    "selection": {
                                        "directReference": {
                                            "structField": {"field": 1},
                                        },
                                        "rootReference": {},
                                    },
                                },
                            },
                        ],
                        "outputType": {"i64": {"nullability": "NULLABILITY_NULLABLE"}},
                    }
                },
            ],
        }
    }
    assert to_dict(result) == expected


def test_emit_mutate_select_all(compiler):
    t = ibis.table([("a", "int64"), ("b", "char"), ("c", "int32")], name="table0")
    expr = t.mutate(d=t.a + 1)
    result = translate(expr, compiler=compiler)
    expected = {
        "project": {
            "common": {"emit": {"outputMapping": [3, 4, 5, 6]}},
            "input": {
                "read": {
                    "common": {"direct": {}},
                    "baseSchema": {
                        "names": ["a", "b", "c"],
                        "struct": {
                            "types": [
                                {"i64": {"nullability": "NULLABILITY_NULLABLE"}},
                                {"string": {"nullability": "NULLABILITY_NULLABLE"}},
                                {"i32": {"nullability": "NULLABILITY_NULLABLE"}},
                            ],
                            "nullability": "NULLABILITY_REQUIRED",
                        },
                    },
                    "namedTable": {"names": ["table0"]},
                }
            },
            "expressions": [
                {
                    "selection": {
                        "directReference": {"structField": {}},
                        "rootReference": {},
                    }
                },
                {
                    "selection": {
                        "directReference": {"structField": {"field": 1}},
                        "rootReference": {},
                    }
                },
                {
                    "selection": {
                        "directReference": {"structField": {"field": 2}},
                        "rootReference": {},
                    }
                },
                {
                    "scalarFunction": {
                        "functionReference": 1,
                        "outputType": {"i64": {"nullability": "NULLABILITY_NULLABLE"}},
                        "arguments": [
                            {
                                "value": {
                                    "selection": {
                                        "directReference": {"structField": {}},
                                        "rootReference": {},
                                    }
                                },
                            },
                            {
                                "value": {
                                    "cast": {
                                        "failureBehavior": "FAILURE_BEHAVIOR_THROW_EXCEPTION",
                                        "input": {"literal": {"i8": 1}},
                                        "type": {
                                            "i64": {
                                                "nullability": "NULLABILITY_NULLABLE"
                                            }
                                        },
                                    }
                                }
                            },
                        ],
                    }
                },
            ],
        }
    }

    assert to_dict(result) == expected


def test_emit_nested_projection_output_mapping(compiler):
    t = ibis.table(
        [
            ("a", "int64"),
            ("b", "int64"),
            ("c", "int64"),
            ("d", "int64"),
        ],
        name="t",
    )
    expr = t["a", "b", "c", "d"]
    result = translate(expr, compiler=compiler)
    # root table has 4 columns, so output mapping starts at index 4
    # should have 4 entries
    assert result.project.common.emit.output_mapping == [4, 5, 6, 7]

    expr = expr["a", "b", "c"]
    result = translate(expr, compiler=compiler)
    # previous emit has 4 columns, so output mapping starts at index 4
    # should have 3 entries
    assert result.project.common.emit.output_mapping == [4, 5, 6]

    expr = expr["a", "b"]
    result = translate(expr, compiler=compiler)
    # previous emit has 3 columns, so output mapping starts at index 3
    # should have 2 entries
    assert result.project.common.emit.output_mapping == [3, 4]


def test_aggregate_project_output_mapping(compiler):
    t = ibis.table(
        [
            ("a", "int64"),
            ("b", "int64"),
            ("c", "int64"),
            ("d", "int64"),
            ("e", "int64"),
        ],
        name="t",
    )

    expr = (
        t.group_by(["a", "b"]).aggregate([t.c.sum().name("sum")]).select(["b", "sum"])
    )

    result = translate(expr, compiler=compiler)
    assert result.project.common.emit.output_mapping == [3, 4]

    # Select 3 of 5 columns in base table to make sure output mapping reflects
    # a count from the outputs of the aggregation ('a', 'b', and 'sum')
    expr = (
        t.select(["a", "b", "c"])
        .group_by(["a", "b"])
        .aggregate([t.c.sum().name("sum")])
        .select(["b", "sum"])
    )

    result = translate(expr, compiler=compiler)
    assert result.project.common.emit.output_mapping == [3, 4]


def test_ibis_schema_to_substrait_schema():
    input = ibis.schema(
        [
            (
                "a",
                dt.Array(dt.Struct.from_tuples([("b", "int64"), ("c", "int64")])),
            ),
            (
                "b",
                dt.Array(dt.Struct.from_tuples([("b", "int64"), ("c", "int64")])),
            ),
            ("d", "int64"),
        ]
    )

    expected = stt.NamedStruct(
        names=["a", "b", "c", "b", "b", "c", "d"],
        struct=stt.Type.Struct(
            types=[
                stt.Type(
                    list=stt.Type.List(
                        type=stt.Type(
                            struct=stt.Type.Struct(
                                types=[
                                    stt.Type(
                                        i64=stt.Type.I64(
                                            nullability=NULLABILITY_NULLABLE,
                                        )
                                    ),
                                    stt.Type(
                                        i64=stt.Type.I64(
                                            nullability=NULLABILITY_NULLABLE,
                                        )
                                    ),
                                ],
                                nullability=NULLABILITY_NULLABLE,
                            )
                        ),
                        nullability=NULLABILITY_NULLABLE,
                    )
                ),
                stt.Type(
                    list=stt.Type.List(
                        type=stt.Type(
                            struct=stt.Type.Struct(
                                types=[
                                    stt.Type(
                                        i64=stt.Type.I64(
                                            nullability=NULLABILITY_NULLABLE,
                                        )
                                    ),
                                    stt.Type(
                                        i64=stt.Type.I64(
                                            nullability=NULLABILITY_NULLABLE,
                                        )
                                    ),
                                ],
                                nullability=NULLABILITY_NULLABLE,
                            )
                        ),
                        nullability=NULLABILITY_NULLABLE,
                    )
                ),
                stt.Type(i64=stt.Type.I64(nullability=NULLABILITY_NULLABLE)),
            ],
            nullability=NULLABILITY_REQUIRED,
        ),
    )
    assert translate(input) == expected


@pytest.mark.parametrize(("name", "expected_offset"), [("a", 0), ("b", 1), ("c", 2)])
def test_simple_field_access(compiler, name, expected_offset):
    t = ibis.table(
        dict(
            a="string",
            b="struct<a: string, b: int64, c: float64>",
            c="array<array<float64>>",
        )
    )
    expr = t[name]
    expected = json_format.ParseDict(
        {
            "selection": {
                "direct_reference": {"struct_field": {"field": expected_offset}},
                "root_reference": {},
            }
        },
        stalg.Expression(),
    )
    result = translate(expr, compiler=compiler)
    assert result == expected


@pytest.mark.parametrize(("name", "expected_offset"), [("a", 0), ("b", 1), ("c", 2)])
def test_struct_field_access(compiler, name, expected_offset):
    t = ibis.table(dict(f="struct<a: string, b: int64, c: float64>"))
    expr = t.f[name]
    expected = json_format.ParseDict(
        {
            "selection": {
                "direct_reference": {
                    "struct_field": {
                        "field": 0,
                        "child": {"struct_field": {"field": expected_offset}},
                    }
                },
                "root_reference": {},
            }
        },
        stalg.Expression(),
    )
    result = translate(expr, compiler=compiler)
    assert result == expected


def test_nested_struct_field_access(compiler):
    t = ibis.table(
        dict(f="struct<a: struct<a: int64, b: struct<a: int64, b: int64, c: int64>>>")
    )
    #        0  0    1    2
    expr = t.f["a"]["b"]["c"]
    expected = json_format.ParseDict(
        {
            "selection": {
                "direct_reference": {
                    "struct_field": {
                        "field": 0,
                        "child": {
                            "struct_field": {
                                "field": 0,
                                "child": {
                                    "struct_field": {
                                        "field": 1,
                                        "child": {"struct_field": {"field": 2}},
                                    }
                                },
                            }
                        },
                    }
                },
                "root_reference": {},
            }
        },
        stalg.Expression(),
    )
    result = translate(expr, compiler=compiler)
    assert result == expected


def test_function_argument_usage(compiler):
    t = ibis.table([("a", "int64")], name="t")
    expr = t.a.count()

    result = translate(expr, compiler=compiler)
    # Check that there is an `arguments` field
    # and that it has the expected `value`
    expected = json_format.ParseDict(
        {
            "value": {
                "selection": {
                    "direct_reference": {"struct_field": {}},
                    "root_reference": {},
                },
            },
        },
        stalg.FunctionArgument(),
    )

    assert result.arguments[0] == expected


def test_aggregate_filter_select_output_mapping(compiler):
    t = ibis.table([("a", "int"), ("b", "float"), ("c", "int")], name="t")

    expr = (
        t.aggregate(
            [
                t.a.max().name("amax"),
                t.b.max().name("bmax"),
                t.a.min().name("amin"),
                t.c.min().name("cmin"),
                t.c.max().name("cmax"),
            ],
        )
        .filter(_.amin < 5)
        .select("amin", "bmax")
    )

    # Aggregate of 3 columns with 5 created columns as the output
    # Filter to put an op between aggregate and select
    # Project out two columns, output_mapping should be 5, 6
    # because 0, 1, 2, 3, 4 correspond to the created aggregate cols.
    result = translate(expr, compiler=compiler)

    assert result.project.common.emit.output_mapping == [5, 6]


def test_filter_over_subquery(compiler):
    t = ibis.table([("a", "int")], name="t").filter(_.a > _.a.mean())
    translate(t, compiler=compiler)


def test_groupby_multiple_keys(compiler):
    t = ibis.table(name="t", schema=(("a", "int"), ("b", "int")))
    expr = t.group_by(["a", "b"]).agg()
    plan = translate(expr, compiler=compiler)

    # There should be one grouping with two separate expressions inside
    assert len(plan.aggregate.groupings) == 1
    assert len(plan.aggregate.groupings[0].grouping_expressions) == 2


def test_join_chain_indexing_in_group_by(compiler):
    t1 = ibis.table([("a", int), ("b", int)], name="t1")
    t2 = ibis.table([("a", int), ("c", int)], name="t2")
    t3 = ibis.table([("a", int), ("d", int)], name="t3")
    t4 = ibis.table([("a", int), ("c", int)], name="t4")

    join_chain = t1.join(t2, "a").join(t3, "a").join(t4, "a")
    # Indexing for chained join
    # t1: a: 0
    # t1: b: 1
    # t2: a: 2
    # t2: c: 3
    # t3: a: 4
    # t3: d: 5
    # t4: a: 6
    # t4: c: 7

    expr = join_chain.group_by("d").count().select("d")
    plan = compiler.compile(expr)
    # Check that the field index for the group_by key is correctly indexed
    assert (
        plan.relations[0]
        .root.input.project.input.aggregate.groupings[0]
        .grouping_expressions[0]
        .selection.direct_reference.struct_field.field
        == 5
    )

    expr = join_chain.group_by("c").count().select("c")
    plan = compiler.compile(expr)
    # Check that the field index for the group_by key is correctly indexed
    assert (
        plan.relations[0]
        .root.input.project.input.aggregate.groupings[0]
        .grouping_expressions[0]
        .selection.direct_reference.struct_field.field
        == 3
    )

    # Group-by on a column that will be renamed by the joinchain
    expr = join_chain.group_by(t4.c).count().select("c")
    plan = compiler.compile(expr)
    # Check that the field index for the group_by key is correctly indexed
    assert (
        plan.relations[0]
        .root.input.project.input.aggregate.groupings[0]
        .grouping_expressions[0]
        .selection.direct_reference.struct_field.field
        == 7
    )
