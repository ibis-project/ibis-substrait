from collections import OrderedDict

import ibis
import ibis.expr.datatypes as dt
import pytest
from google.protobuf import json_format
from ibis.udf.vectorized import analytic, elementwise

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
        ]
    )
    # win = ibis.window(preceding=None, following=None, group_by='key')
    expr = tbl.mutate(
        # demean_and_zscore(tbl['value']).over(win).destructure()
        # twice_and_add_2(tbl['value']).destructure()
        twice(tbl["value"]).name("twice")
    )
    result = compiler.compile(expr)
    js = to_dict(result)
    with open("blah", "w") as f:
        f.write(str(js))


def _test_add(add_func, expected):
    from ibis_substrait.compiler.core import SubstraitCompiler
    compiler = SubstraitCompiler(uri="https://github.com/apache/arrow/blob/master/format/substrait/extension_types.yaml")
    tbl = ibis.table({"volume": "double"})
    expr = add_func(tbl)
    result = compiler.compile(expr)
    assert result == expected


def test_udf_add():
    code = (
        "gAWVGgMAAAAAAACMF2Nsb3VkcGlja2xlLmNsb3VkcGlja2xllIwNX2J1aWx0aW5fdHlwZZSTlIwKTGFt" +
        "YmRhVHlwZZSFlFKUKGgCjAhDb2RlVHlwZZSFlFKUKEsBSwBLAEsCSwRLQ0MYZAFkAmwAbQF9AQEAfAGg" +
        "AnwAZAOhAlMAlCiMJENvbXB1dGUgdHdpY2UgdGhlIHZhbHVlIG9mIHRoZSBpbnB1dJRLAE5LAnSUjA9w" +
        "eWFycm93LmNvbXB1dGWUjAdjb21wdXRllIwIbXVsdGlwbHmUh5SMAXaUjAJwY5SGlIxgL21udC91c2Vy" +
        "MS90c2NvbnRyYWN0L2dpdGh1Yi9ydHBzdy9pYmlzLXN1YnN0cmFpdC9pYmlzX3N1YnN0cmFpdC90ZXN0" +
        "cy9jb21waWxlci90ZXN0X2NvbXBpbGVyLnB5lIwFdHdpY2WUTUgBQwQAAwwBlCkpdJRSlH2UKIwLX19w" +
        "YWNrYWdlX1+UjB1pYmlzX3N1YnN0cmFpdC50ZXN0cy5jb21waWxlcpSMCF9fbmFtZV9flIwraWJpc19z" +
        "dWJzdHJhaXQudGVzdHMuY29tcGlsZXIudGVzdF9jb21waWxlcpSMCF9fZmlsZV9flIxgL21udC91c2Vy" +
        "MS90c2NvbnRyYWN0L2dpdGh1Yi9ydHBzdy9pYmlzLXN1YnN0cmFpdC9pYmlzX3N1YnN0cmFpdC90ZXN0" +
        "cy9jb21waWxlci90ZXN0X2NvbXBpbGVyLnB5lHVOTk50lFKUjBxjbG91ZHBpY2tsZS5jbG91ZHBpY2ts" +
        "ZV9mYXN0lIwSX2Z1bmN0aW9uX3NldHN0YXRllJOUaCB9lH2UKGgbaBSMDF9fcXVhbG5hbWVfX5RoFIwP" +
        "X19hbm5vdGF0aW9uc19flH2UjA5fX2t3ZGVmYXVsdHNfX5ROjAxfX2RlZmF1bHRzX1+UTowKX19tb2R1" +
        "bGVfX5RoHIwHX19kb2NfX5RoCowLX19jbG9zdXJlX1+UTowXX2Nsb3VkcGlja2xlX3N1Ym1vZHVsZXOU" +
        "XZSMC19fZ2xvYmFsc19flH2UdYaUhlIwLg=="
    )
    expected = json_format.ParseDict(
        {
          "extensionUris": [
            {
              "extensionUriAnchor": 1,
              "uri": "https://github.com/apache/arrow/blob/master/format/substrait/extension_types.yaml"
            }
          ],
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
                    {
                      "fp64": {
                        "nullability": "NULLABILITY_NULLABLE"
                      }
                    }
                  ],
                  "outputType": {
                    "fp64": {
                      "nullability": "NULLABILITY_NULLABLE"
                    }
                  }
                }
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
                          "names": [
                            "volume"
                          ],
                          "struct": {
                            "types": [
                              {
                                "fp64": {
                                  "nullability": "NULLABILITY_NULLABLE"
                                }
                              }
                            ],
                            "nullability": "NULLABILITY_REQUIRED"
                          }
                        },
                        "namedTable": {
                          "names": [
                            "unbound_table_0"
                          ]
                        }
                      }
                    },
                    "expressions": [
                      {
                        "selection": {
                          "directReference": {
                            "structField": {}
                          },
                          "rootReference": {}
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
                                "rootReference": {}
                              }
                            }
                          ],
                          "outputType": {
                            "fp64": {
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }
                        }
                      }
                    ]
                  }
                },
                "names": [
                  "volume",
                  "twice_volume"
                ]
              }
            }
          ]
        },
        stpln.Plan(),
    )
    add_func = lambda tbl: tbl.mutate(twice(tbl["volume"]).name("twice_volume"))
    _test_add(add_func, expected)


def test_reg_add():
    expected = json_format.ParseDict(
        {
          "extensionUris": [
            {
              "extensionUriAnchor": 1,
              "uri": "https://github.com/apache/arrow/blob/master/format/substrait/extension_types.yaml"
            }
          ],
          "extensions": [
            {
              "extensionFunction": {
                "extensionUriReference": 1,
                "functionAnchor": 1,
                "name": "*"
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
                          "names": [
                            "volume"
                          ],
                          "struct": {
                            "types": [
                              {
                                "fp64": {
                                  "nullability": "NULLABILITY_NULLABLE"
                                }
                              }
                            ],
                            "nullability": "NULLABILITY_REQUIRED"
                          }
                        },
                        "namedTable": {
                          "names": [
                            "unbound_table_0"
                          ]
                        }
                      }
                    },
                    "expressions": [
                      {
                        "selection": {
                          "directReference": {
                            "structField": {}
                          },
                          "rootReference": {}
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
                                "rootReference": {}
                              }
                            },
                            {
                              "literal": {
                                "i8": 2
                              }
                            }
                          ],
                          "outputType": {
                            "fp64": {
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }
                        }
                      }
                    ]
                  }
                },
                "names": [
                  "volume",
                  "twice_volume"
                ]
              }
            }
          ]
        },
        stpln.Plan(),
    )
    add_func = lambda tbl: tbl.mutate(twice_volume=tbl["volume"] * 2)
    _test_add(add_func, expected)
