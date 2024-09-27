from ibis_substrait.compiler.extension_language import evaluate


def test_simple_arithmetic():
    assert evaluate("1 + 1") == 2


def test_simple_arithmetic_with_variables():
    assert evaluate("1 + var", {"var": 2}) == 3


def test_simple_arithmetic_precedence():
    assert evaluate("1 + var * 3", {"var": 2}) == 7


def test_simple_arithmetic_parenthesis():
    assert evaluate("(1 + var) * 3", {"var": 2}) == 9


def test_min_max():
    assert evaluate("min(var, 7) + max(var, 7) * 2", {"var": 5}) == 19


def test_ternary():
    assert evaluate("var > 3 ? 1 : 0", {"var": 5}) == 1
    assert evaluate("var > 3 ? 1 : 0", {"var": 2}) == 0


def test_multiline():
    assert (
        evaluate(
            """
                    temp = min(var, 7) + max(var, 7) * 2
                    temp + 1
                    """,
            {"var": 5},
        )
        == 20
    )


def test_data_type():
    assert evaluate("decimal<S + 1, P + 1>", {"S": 20, "P": 10}) == "decimal<21,11>"


def test_decimal_example():
    def func(P1, S1, P2, S2):
        init_scale = max(S1, S2)  # 14
        init_prec = init_scale + max(P1 - S1, P2 - S2) + 1
        min_scale = min(init_scale, 6)
        delta = init_prec - 38
        prec = min(init_prec, 38)
        scale_after_borrow = max(init_scale - delta, min_scale)
        scale = scale_after_borrow if init_prec > 38 else init_scale
        return f"DECIMAL<{prec},{scale}>"

    args = {"P1": 10, "S1": 8, "P2": 14, "S2": 2}

    assert evaluate(
        """
                    init_scale = max(S1,S2)
                    init_prec = init_scale + max(P1 - S1, P2 - S2) + 1
                    min_scale = min(init_scale, 6)
                    delta = init_prec - 38
                    prec = min(init_prec, 38)
                    scale_after_borrow = max(init_scale - delta, min_scale)
                    scale = init_prec > 38 ? scale_after_borrow : init_scale
                    DECIMAL<prec, scale>
                    """,
        args,
    ) == func(**args)
