import base64
from collections import OrderedDict

import cloudpickle
import ibis
import ibis.expr.datatypes as dt
import pytest
from google.protobuf import json_format
from ibis.udf.table import tabular
from ibis.udf.vectorized import analytic, elementwise

from ibis_substrait.compiler.translate import translate
from ibis_substrait.proto.substrait import algebra_pb2 as stalg
from ibis_substrait.proto.substrait import plan_pb2 as stpln
from ibis_substrait.proto.substrait import type_pb2 as stt

NULLABILITY_NULLABLE = stt.Type.Nullability.NULLABILITY_NULLABLE
NULLABILITY_REQUIRED = stt.Type.Nullability.NULLABILITY_REQUIRED

_URI = (
    "https://github.com/apache/arrow/blob/master/format/substrait/extension_types.yaml"
)


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


@analytic(input_type=[dt.double], output_type=dt.double)
def zscore(series):  # note the use of aggregate functions
    return (series - series.mean()) / series.std()


@analytic(
    input_type=[dt.double],
    output_type=dt.Struct(["demean", "zscore"], [dt.double, dt.double]),
)
def demean_and_zscore(v):
    """Compute demeaned and zscore values of the input"""
    mean = v.mean()
    std = v.std()
    return v - mean, (v - mean) / std


@elementwise(
    input_type=[dt.double],
    output_type=dt.Struct(["twice", "add_2"], [dt.double, dt.double]),
)
def twice_and_add_2(v):
    """Compute twice and add_2 values of the input"""
    import pyarrow.compute as pc

    return pc.multiply(v, 2), pc.add(v, 2)


@elementwise(input_type=[dt.double], output_type=dt.double)
def twice(v):
    """Compute twice the value of the input"""
    import pyarrow.compute as pc

    return pc.multiply(v, 2)


def test_vectorized_udf(t, compiler):
    tbl = ibis.table(
        [
            ("key", "string"),
            ("value", "int64"),
        ],
        name="unbound_table",
    )
    # win = ibis.window(preceding=None, following=None, group_by='key')
    expr = tbl.mutate(
        # demean_and_zscore(tbl['value']).over(win).destructure()
        # twice_and_add_2(tbl['value']).destructure()
        twice(tbl["value"]).name("twice")
    )

    code = base64.b64encode(cloudpickle.dumps(twice.func)).decode("utf-8")
    nullable = {"nullability": "NULLABILITY_NULLABLE"}
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
                            "inputTypes": [{"fp64": nullable}],
                            "outputType": {"fp64": nullable},
                            "scalar": {},
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
                                                    {"string": nullable},
                                                    {"i64": nullable},
                                                ],
                                                "nullability": "NULLABILITY_REQUIRED",
                                            },
                                        },
                                        "namedTable": {"names": ["unbound_table"]},
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
                                            "outputType": {"fp64": nullable},
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


def _test_add(add_func, expected):
    from ibis_substrait.compiler.core import SubstraitCompiler

    compiler = SubstraitCompiler(uri=_URI)
    tbl = ibis.table({"volume": "double"}, name="an_unbound_table")
    expr = add_func(tbl)
    result = compiler.compile(expr)
    assert result == expected


def test_udf_add():
    code = base64.b64encode(cloudpickle.dumps(twice.func)).decode("utf-8")
    nullable = {"nullability": "NULLABILITY_NULLABLE"}
    expected = json_format.ParseDict(
        {
            "extensionUris": [{"extensionUriAnchor": 1, "uri": _URI}],
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
                            "inputTypes": [
                                {"fp64": {"nullability": "NULLABILITY_NULLABLE"}}
                            ],
                            "outputType": {
                                "fp64": {"nullability": "NULLABILITY_NULLABLE"}
                            },
                            "scalar": {},
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
                                            "names": ["volume"],
                                            "struct": {
                                                "types": [{"fp64": nullable}],
                                                "nullability": "NULLABILITY_REQUIRED",
                                            },
                                        },
                                        "namedTable": {"names": ["an_unbound_table"]},
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
                                        "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [
                                                {
                                                    "selection": {
                                                        "directReference": {
                                                            "structField": {}
                                                        },
                                                        "rootReference": {},
                                                    }
                                                }
                                            ],
                                            "outputType": {"fp64": nullable},
                                        }
                                    },
                                ],
                            }
                        },
                        "names": ["volume", "twice_volume"],
                    }
                }
            ],
        },
        stpln.Plan(),
    )

    def add_func(tbl):
        return tbl.mutate(twice(tbl["volume"]).name("twice_volume"))

    _test_add(add_func, expected)


def test_reg_add():
    nullable = {"nullability": "NULLABILITY_NULLABLE"}
    expected = json_format.ParseDict(
        {
            "extensionUris": [{"extensionUriAnchor": 1, "uri": _URI}],
            "extensions": [
                {
                    "extensionFunction": {
                        "extensionUriReference": 1,
                        "functionAnchor": 1,
                        "name": "*",
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
                                            "names": ["volume"],
                                            "struct": {
                                                "types": [{"fp64": nullable}],
                                                "nullability": "NULLABILITY_REQUIRED",
                                            },
                                        },
                                        "namedTable": {"names": ["an_unbound_table"]},
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
                                        "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [
                                                {
                                                    "selection": {
                                                        "directReference": {
                                                            "structField": {}
                                                        },
                                                        "rootReference": {},
                                                    }
                                                },
                                                {"literal": {"i8": 2}},
                                            ],
                                            "outputType": {"fp64": nullable},
                                        }
                                    },
                                ],
                            }
                        },
                        "names": ["volume", "twice_volume"],
                    }
                }
            ],
        },
        stpln.Plan(),
    )

    def add_func(tbl):
        return tbl.mutate(twice_volume=tbl["volume"] * 2)

    _test_add(add_func, expected)


@tabular(
    output_type=dt.Struct(["x", "y"], [dt.double, dt.double]),
)
def x_y_table():
    """Source a table with x and y columns"""
    import numpy as np
    import pandas as pd

    return pd.DataFrame(
        np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float64), columns=["x", "y"]
    )


def test_udt():
    from ibis_substrait.compiler.core import SubstraitCompiler

    compiler = SubstraitCompiler(uri=_URI)
    expr = x_y_table()
    code = base64.b64encode(cloudpickle.dumps(x_y_table.func)).decode("utf-8")
    nullable = {"nullability": "NULLABILITY_NULLABLE"}
    expected = json_format.ParseDict(
        {
            "extensionUris": [{"extensionUriAnchor": 1, "uri": _URI}],
            "extensions": [
                {
                    "extensionFunction": {
                        "extensionUriReference": 1,
                        "functionAnchor": 1,
                        "name": "x_y_table",
                        "udf": {
                            "code": code,
                            "summary": "x_y_table",
                            "description": "Source a table with x and y columns",
                            "inputTypes": [],
                            "outputType": {
                                "struct": {
                                    "types": [
                                        {"fp64": nullable},
                                        {"fp64": nullable},
                                    ],
                                    "nullability": "NULLABILITY_NULLABLE",
                                }
                            },
                            "tabular": {},
                        },
                    }
                }
            ],
            "relations": [
                {
                    "root": {
                        "input": {
                            "read": {
                                "baseSchema": {
                                    "names": ["x", "y"],
                                    "struct": {
                                        "types": [
                                            {"fp64": nullable},
                                            {"fp64": nullable},
                                        ],
                                        "nullability": "NULLABILITY_REQUIRED",
                                    },
                                },
                                "udt": {"function_reference": 1},
                            }
                        },
                        "names": ["x", "y"],
                    }
                }
            ],
        },
        stpln.Plan(),
    )
    result = compiler.compile(expr)
    assert result == expected
