import datetime
import decimal
import uuid
from collections import OrderedDict

import ibis
import ibis.expr.datatypes as dt
import pytest
import pytz

from ibis_substrait.compiler.decompile import decompile
from ibis_substrait.compiler.translate import _date_to_days, _time_to_micros, translate
from ibis_substrait.proto.substrait import expression_pb2 as stexpr
from ibis_substrait.proto.substrait import type_pb2 as stt

NULLABILITY_NULLABLE = stt.Type.Nullability.NULLABILITY_NULLABLE

TIMESTAMP = datetime.datetime(
    year=2021,
    month=11,
    day=15,
    hour=1,
    minute=2,
    second=3,
    microsecond=42,
)
MICROSECONDS_SINCE_EPOCH = int(TIMESTAMP.timestamp() * 1e6)
DATE = TIMESTAMP.date()
DATE_DAYS = _date_to_days(DATE)
TIME = TIMESTAMP.time()
TIME_MICROS = _time_to_micros(TIME)
UUID = uuid.uuid4()


literal_cases = pytest.mark.parametrize(
    ("expr", "ir"),
    [
        # booleans
        pytest.param(
            ibis.literal(True),
            stexpr.Expression(literal=stexpr.Expression.Literal(boolean=True)),
            id="boolean_true",
        ),
        pytest.param(
            ibis.literal(False),
            stexpr.Expression(literal=stexpr.Expression.Literal(boolean=False)),
            id="boolean_false",
        ),
    ]
    + [
        # integers
        pytest.param(
            ibis.literal(value),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(**{substrait_type: value})
            ),
            id=f"{substrait_type}_{value_name}",
        )
        for ibis_type, substrait_type in [
            (dt.int8, "i8"),
            (dt.int16, "i16"),
            (dt.int32, "i32"),
            (dt.int64, "i64"),
        ]
        for value_name, value in ibis_type.bounds._asdict().items()
    ]
    + [
        # floating point
        pytest.param(
            ibis.literal(1.0, type="float64"),
            stexpr.Expression(literal=stexpr.Expression.Literal(fp64=1.0)),
            id="fp64",
        ),
        pytest.param(
            ibis.literal(2.0, type="float32"),
            stexpr.Expression(literal=stexpr.Expression.Literal(fp32=2.0)),
            id="fp32",
        ),
        # strings
        pytest.param(
            ibis.literal("foo"),
            stexpr.Expression(literal=stexpr.Expression.Literal(string="foo")),
            id="string",
        ),
        pytest.param(
            ibis.literal("⋃"),
            stexpr.Expression(literal=stexpr.Expression.Literal(string="⋃")),
            id="unicode_string",
        ),
        # binary
        pytest.param(
            ibis.literal(b"42", type="binary"),
            stexpr.Expression(literal=stexpr.Expression.Literal(binary=b"42")),
            id="binary",
        ),
        # timestamp
        pytest.param(
            ibis.timestamp(TIMESTAMP),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    timestamp=int(MICROSECONDS_SINCE_EPOCH)
                ),
            ),
            id="timestamp",
        ),
        pytest.param(
            ibis.timestamp(
                datetime.datetime.fromtimestamp(TIMESTAMP.timestamp(), tz=pytz.utc),
                timezone="UTC",
            ),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    timestamp_tz=int(MICROSECONDS_SINCE_EPOCH)
                ),
            ),
            id="timestamp_tz",
        ),
        # date
        pytest.param(
            ibis.date(DATE),
            stexpr.Expression(literal=stexpr.Expression.Literal(date=DATE_DAYS)),
            id="date",
        ),
        # time
        pytest.param(
            ibis.time(TIME),
            stexpr.Expression(literal=stexpr.Expression.Literal(time=TIME_MICROS)),
            id="time",
        ),
    ]
    + [
        # interval_year_to_month
        pytest.param(
            ibis.interval(**{key: value}),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    interval_year_to_month=(
                        stexpr.Expression.Literal.IntervalYearToMonth(**{key: value})
                    )
                ),
            ),
            id=f"interval_year_to_month_{key}",
            marks=[pytest.mark.xfail(raises=NotImplementedError)],
        )
        for key, value in [("years", 84), ("months", 42)]
    ]
    + [
        # interval_day_to_second
        pytest.param(
            ibis.interval(**{key: value}),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    interval_day_to_second=(
                        stexpr.Expression.Literal.IntervalDayToSecond(**{key: value})
                    )
                ),
            ),
            id=f"interval_day_to_second_{key}",
            marks=[pytest.mark.xfail(raises=NotImplementedError)],
        )
        for key, value in [("days", 84), ("seconds", 42)]
    ]
    + [
        # fixed_char: not representable in ibis
        # var_char: not representable in ibis
        # fixed_binary: not representable in ibis
        # struct
        pytest.param(
            ibis.literal(OrderedDict(a=1.0, b=[2.0])),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    struct=stexpr.Expression.Literal.Struct(
                        fields=[
                            stexpr.Expression.Literal(fp64=1.0),
                            stexpr.Expression.Literal(
                                list=stexpr.Expression.Literal.List(
                                    values=[stexpr.Expression.Literal(fp64=2.0)],
                                )
                            ),
                        ]
                    )
                ),
            ),
            id="struct",
            marks=[pytest.mark.no_decompile],
        ),
        # map
        pytest.param(
            ibis.literal(dict(a=[], b=[2])),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    map=stexpr.Expression.Literal.Map(
                        key_values=[
                            stexpr.Expression.Literal.Map.KeyValue(
                                key=stexpr.Expression.Literal(string="a"),
                                value=stexpr.Expression.Literal(
                                    empty_list=stt.Type.List(
                                        type=stt.Type(
                                            i8=stt.Type.I8(
                                                nullability=NULLABILITY_NULLABLE
                                            )
                                        ),
                                        nullability=NULLABILITY_NULLABLE,
                                    ),
                                ),
                            ),
                            stexpr.Expression.Literal.Map.KeyValue(
                                key=stexpr.Expression.Literal(string="b"),
                                value=stexpr.Expression.Literal(
                                    list=stexpr.Expression.Literal.List(
                                        values=[stexpr.Expression.Literal(i8=2)],
                                    )
                                ),
                            ),
                        ],
                    )
                ),
            ),
            id="map",
        ),
        # empty map
        pytest.param(
            ibis.literal({}, type="map<string, int64>"),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    empty_map=stt.Type.Map(
                        key=stt.Type(
                            string=stt.Type.String(nullability=NULLABILITY_NULLABLE)
                        ),
                        value=stt.Type(
                            i64=stt.Type.I64(nullability=NULLABILITY_NULLABLE)
                        ),
                        nullability=NULLABILITY_NULLABLE,
                    )
                )
            ),
            id="empty_map",
        ),
    ]
    + [
        # uuid
        pytest.param(
            ibis.literal(UUID, type=dt.uuid),
            stexpr.Expression(literal=stexpr.Expression.Literal(uuid=UUID.bytes)),
            id="uuid_typed",
        ),
        pytest.param(
            ibis.literal(str(UUID), type=dt.uuid),
            stexpr.Expression(literal=stexpr.Expression.Literal(uuid=UUID.bytes)),
            id="uuid_string",
        ),
    ]
    + [
        # null
        pytest.param(
            ibis.literal(None, type="float64"),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    null=stt.Type(fp64=stt.Type.FP64(nullability=NULLABILITY_NULLABLE))
                )
            ),
            id="null_fp64",
        ),
        pytest.param(
            ibis.literal(None, type="array<string>"),
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    null=stt.Type(
                        list=stt.Type.List(
                            type=stt.Type(
                                string=stt.Type.String(nullability=NULLABILITY_NULLABLE)
                            ),
                            nullability=NULLABILITY_NULLABLE,
                        )
                    )
                ),
            ),
            id="null_array",
        ),
        # list
        pytest.param(
            ibis.literal(["a", "b"]),  # called Array in ibis
            stexpr.Expression(
                literal=stexpr.Expression.Literal(
                    list=stexpr.Expression.Literal.List(
                        values=[
                            stexpr.Expression.Literal(string="a"),
                            stexpr.Expression.Literal(string="b"),
                        ],
                    )
                ),
            ),
            id="array",
        ),
    ],
)


@literal_cases
def test_literal(compiler, expr, ir):
    result = translate(expr, compiler)
    assert result.SerializeToString() == ir.SerializeToString()


@pytest.mark.xfail(
    raises=ibis.common.exceptions.IbisTypeError,
    reason="Ibis doesn't allow decimal values through validation",
)
def test_decimal_literal(compiler):
    # TODO: ibis doesn't validate a decimal.Decimal's value against the
    # provided decimal type
    expr = ibis.literal(decimal.Decimal("234.234"), type="decimal(6, 3)")
    ir = stexpr.Expression(
        literal=stexpr.Expression.Literal(
            decimal=stexpr.Expression.Literal.Decimal(
                value=b"234.234", precision=6, scale=3
            )
        )
    )
    result = translate(expr, compiler)
    assert result.SerializeToString() == ir.SerializeToString()


@pytest.mark.parametrize("value", [ibis.NA, ibis.literal(None)])
def test_bare_null(compiler, value):
    with pytest.raises(NotImplementedError, match="untyped null literals"):
        translate(value, compiler)


@literal_cases
def test_decompile(expr, ir):
    value, dtype = decompile(ir.literal)
    result = ibis.literal(value, type=dtype)
    assert result.equals(expr)
