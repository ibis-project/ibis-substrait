from collections import OrderedDict

import ibis
import ibis.expr.datatypes as dt
import pytest
from google.protobuf import json_format
from ibis.udf.vectorized import elementwise

from ibis_substrait.compiler.translate import translate
from ibis_substrait.proto.substrait import algebra_pb2 as stalg
from ibis_substrait.proto.substrait import plan_pb2 as stpln
from ibis_substrait.proto.substrait import type_pb2 as stt

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
    result = translate(expr, compiler)
    js = to_dict(result)
    assert js


def test_aggregation_with_sort(t, compiler):
    expr = (
        t.group_by(name_len=lambda t: t.full_name.length())
        .aggregate(max_age=t.age.max(), min_age=t.age.min())
        .sort_by("ts")
        .filter(lambda t: t.name_len > 3)
    )
    result = translate(expr, compiler)
    js = to_dict(result)
    assert js


def test_aggregation_no_args(t, compiler):
    expr = t.group_by("age").count()
    result = translate(expr, compiler)
    js = to_dict(result)
    assert js


def test_aggregation_window(t, compiler):
    expr = t.projection([t.full_name.length().mean().over(ibis.window(group_by="age"))])
    result = translate(expr, compiler)
    js = to_dict(result)
    assert js


def test_array_literal(compiler):
    expr = ibis.literal(["a", "b"])
    result = translate(expr, compiler)
    js = to_dict(result)
    assert js


def test_map_literal(compiler):
    expr = ibis.literal(dict(a=[], b=[2]))
    result = translate(expr, compiler)
    js = to_dict(result)
    assert js


def test_struct_literal(compiler):
    expr = ibis.literal(OrderedDict(a=1, b=[2.0]))
    result = translate(expr, compiler)
    js = to_dict(result)
    assert js


def test_translate_table_expansion(compiler):
    t = ibis.table([("a", "int32"), ("b", "int64")], name="table0")
    expr = t.mutate(c=t.a + t.b)
    result = translate(expr, compiler)
    expected = {
        "project": {
            "input": {
                "read": {
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
                        "args": [
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
                        ],
                        "outputType": {"i64": {"nullability": "NULLABILITY_NULLABLE"}},
                    }
                },
            ],
        }
    }
    assert to_dict(result) == expected


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
    result = translate(expr, compiler)
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
    result = translate(expr, compiler)
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
    result = translate(expr, compiler)
    assert result == expected


@elementwise(input_type=[dt.double], output_type=dt.double)
def twice(v):
    """Compute twice the value of the input"""
    return 2 * v


def test_vectorized_udf(t, compiler):
    tbl = ibis.table(
        [
            ("key", "string"),
            ("value", "int64"),
        ]
    )
    expr = tbl.mutate(twice(tbl["value"]).name("twice"))
    code = (
        "gAWV1wIAAAAAAACMF2Nsb3VkcGlja2xlLmNsb3VkcGlja2xllIwNX2J1aWx0aW5fdHlwZZST"
        + "lIwKTGFtYmRhVHlwZZSFlFKUKGgCjAhDb2RlVHlwZZSFlFKUKEsBSwBLAEsBSwJLQ0MIZAF8"
        + "ABQAUwCUjCRDb21wdXRlIHR3aWNlIHRoZSB2YWx1ZSBvZiB0aGUgaW5wdXSUSwKGlCmMAXaU"
        + "hZSMYC9tbnQvdXNlcjEvdHNjb250cmFjdC9naXRodWIvcnRwc3cvaWJpcy1zdWJzdHJhaXQv"
        + "aWJpc19zdWJzdHJhaXQvdGVzdHMvY29tcGlsZXIvdGVzdF9jb21waWxlci5weZSMBXR3aWNl"
        + "lE0uAUMCAAOUKSl0lFKUfZQojAtfX3BhY2thZ2VfX5SMHWliaXNfc3Vic3RyYWl0LnRlc3Rz"
        + "LmNvbXBpbGVylIwIX19uYW1lX1+UjCtpYmlzX3N1YnN0cmFpdC50ZXN0cy5jb21waWxlci50"
        + "ZXN0X2NvbXBpbGVylIwIX19maWxlX1+UjGAvbW50L3VzZXIxL3RzY29udHJhY3QvZ2l0aHVi"
        + "L3J0cHN3L2liaXMtc3Vic3RyYWl0L2liaXNfc3Vic3RyYWl0L3Rlc3RzL2NvbXBpbGVyL3Rl"
        + "c3RfY29tcGlsZXIucHmUdU5OTnSUUpSMHGNsb3VkcGlja2xlLmNsb3VkcGlja2xlX2Zhc3SU"
        + "jBJfZnVuY3Rpb25fc2V0c3RhdGWUk5RoG32UfZQoaBZoD4wMX19xdWFsbmFtZV9flGgPjA9f"
        + "X2Fubm90YXRpb25zX1+UfZSMDl9fa3dkZWZhdWx0c19flE6MDF9fZGVmYXVsdHNfX5ROjApf"
        + "X21vZHVsZV9flGgXjAdfX2RvY19flGgKjAtfX2Nsb3N1cmVfX5ROjBdfY2xvdWRwaWNrbGVf"
        + "c3VibW9kdWxlc5RdlIwLX19nbG9iYWxzX1+UfZR1hpSGUjAu"
    )
    nullable = "NULLABILITY_NULLABLE"
    expected = json_format.ParseDict(
        {
            "extensionUris": [{"extensionUriAnchor": 1}],
            "extensions": [
                {
                    "extensionFunction": {
                        "extensionUriReference": 1,
                        "functionAnchor": 1,
                        "name": "twice",
                        "udf": {
                            "code": code,
                            "summary": "twice",
                            "description": "Compute twice the value of the input",
                            "inputTypes": [{"fp64": {"nullability": nullable}}],
                            "outputType": {"fp64": {"nullability": nullable}},
                        },
                    }
                }
            ],
            "relations": [
                {
                    "root": {
                        "input": {
                            "project": {
                                "input": {
                                    "read": {
                                        "baseSchema": {
                                            "names": ["key", "value"],
                                            "struct": {
                                                "types": [
                                                    {
                                                        "string": {
                                                            "nullability": nullable
                                                        }
                                                    },
                                                    {"i64": {"nullability": nullable}},
                                                ],
                                                "nullability": "NULLABILITY_REQUIRED",
                                            },
                                        },
                                        "namedTable": {"names": ["unbound_table_12"]},
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
                                            "directReference": {
                                                "structField": {"field": 1}
                                            },
                                            "rootReference": {},
                                        }
                                    },
                                    {
                                        "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [
                                                {
                                                    "selection": {
                                                        "directReference": {
                                                            "structField": {"field": 1}
                                                        },
                                                        "rootReference": {},
                                                    }
                                                }
                                            ],
                                            "outputType": {
                                                "fp64": {"nullability": nullable}
                                            },
                                        }
                                    },
                                ],
                            }
                        },
                        "names": ["key", "value", "twice"],
                    }
                }
            ],
        },
        stpln.Plan(),
    )
    result = compiler.compile(expr)
    assert result == expected
