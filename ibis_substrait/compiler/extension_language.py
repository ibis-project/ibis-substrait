from typing import Optional, Union

from pyparsing import (
    Forward,
    Group,
    Literal,
    ParseResults,
    Word,
    ZeroOrMore,
    alphas,
    identchars,
    infix_notation,
    nums,
    oneOf,
    opAssoc,
    pyparsing_common,
)

supported_functions = ["max", "min"]

multop = oneOf("* /")
plusop = oneOf("+ -")
compop = oneOf("> <")
assign = Word(identchars + nums)("assign")
variable = Word(identchars + nums)("variable")
integer = Word(nums)
expr = Forward()
fn = Group(
    oneOf(supported_functions)("fn")
    + Literal("(").suppress()
    + expr
    + Literal(",").suppress()
    + expr
    + Literal(")").suppress()
)
dtype = Group(
    Word(alphas)("dtype")
    + Literal("<").suppress()
    + expr
    + Literal(",").suppress()
    + expr
    + Literal(">").suppress()
)

operand = pyparsing_common.integer | fn | dtype | Group(variable)

expr << infix_notation(
    operand,
    [
        (multop, 2, opAssoc.LEFT),
        (plusop, 2, opAssoc.LEFT),
        (compop, 2, opAssoc.LEFT),
        (("?", ":"), 3, opAssoc.RIGHT),
    ],
)

multiline_expr = ZeroOrMore(
    Group(assign + Literal("=").suppress() + Group(expr))
) + expr("result")


def evaluate_pr(pr: ParseResults, values: dict) -> Union[str, int, dict]:
    pr_dict = pr.as_dict()
    tokens = []

    for x in pr:
        evaluated = evaluate_pr(x, values) if isinstance(x, ParseResults) else x
        if isinstance(evaluated, dict):
            values = {**values, **evaluated}
        tokens.append(evaluated)

    if "assign" in pr_dict:
        return {pr_dict["assign"]: tokens[1]}
    elif "fn" in pr_dict:
        if pr_dict["fn"] == "min":
            return min(tokens[1], tokens[2])
        if pr_dict["fn"] == "max":
            return max(tokens[1], tokens[2])
    elif "variable" in pr_dict:
        return values[pr_dict["variable"]]
    elif "dtype" in pr_dict:
        return f"{tokens[0]}<{','.join([str(x) for x in tokens[1:]])}>"
    elif "result" in pr_dict:
        return tokens[-1]

    acc = tokens[0]
    for i in range(len(tokens)):
        if i % 2 != 0:
            if tokens[i] == "*":
                acc = acc * tokens[i + 1]
            elif tokens[i] == "/":
                acc = acc / tokens[i + 1]
            elif tokens[i] == "+":
                acc = acc + tokens[i + 1]
            elif tokens[i] == "-":
                acc = acc - tokens[i + 1]
            elif tokens[i] == ">":
                return acc > tokens[i + 1]
            elif tokens[i] == "<":
                return acc < tokens[i + 1]
            elif tokens[i] == "?":
                return tokens[i + 1] if acc else tokens[i + 3]
            else:
                raise Exception(f"Unknown {tokens[i]}")

    return acc


def evaluate(txt: str, values: Optional[dict] = None) -> Union[str, int]:
    if not values:
        values = {}
    result = evaluate_pr(multiline_expr.parseString(txt), values)
    assert isinstance(result, (int, str))
    return result
