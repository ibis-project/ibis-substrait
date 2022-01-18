from collections import OrderedDict

import ibis
import ibis.expr.datatypes as dt
import pytest
from google.protobuf import json_format

from ibis_substrait.compiler.translate import translate
from ibis_substrait.proto.substrait import type_pb2 as stt

NULLABILITY_NULLABLE = stt.Type.Nullability.NULLABILITY_NULLABLE


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
            ]
        ),
    )
    assert translate(input) == expected
