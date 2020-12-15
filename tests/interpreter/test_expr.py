from computation.interpreter.expressions import (
    Add,
    Boolean,
    Multiply,
    LessThan,
    Number,
    Variable,
)


def test_number():
    assert Number(3) == Number(3)
    assert Number(3) != Number(4)
    assert Number(2) < Number(4)
    assert Number(4) > Number(2)


def test_boolean():
    assert Boolean(True) and Boolean(True)
    assert Boolean(True), Boolean(True)
    assert Boolean(False), Boolean(False)
    assert Boolean(True) != Boolean(False)


def test_add():
    expr = Add(Variable("x"), Variable("y"))
    en = {"x": Number(1), "y": Number(2)}
    while expr.reducible:
        expr = expr.reduce(en)
    assert expr == Number(3)


def test_mul():
    expr = Multiply(Variable("x"), Variable("y"))
    en = {"x": Number(3), "y": Number(4)}
    while expr.reducible:
        expr = expr.reduce(en)
    assert expr == Number(12)


def test_less():
    expr = LessThan(Variable("x"), Variable("y"))
    en = {"x": Number(1), "y": Number(3)}
    while expr.reducible:
        expr = expr.reduce(en)
    assert expr == Boolean(True)


def test_type():
    assert Number(23).evaluate({}) == Number(23)
    assert Variable("x").evaluate({"x": Number(23)}) == Number(23)
    assert LessThan(Add(Variable("x"), Number(2)), Variable("y")).evaluate(
        {"x": Number(2), "y": Number(5)}
    )

    n1 = Number(5)
    b1 = Boolean(False)
    v1 = Variable("x")

    assert eval(n1.to_python)({}) == 5
    assert not eval(b1.to_python)({})
    assert eval(v1.to_python)({"x": 7}) == 7


def test_expr():
    a1 = Add(Variable("x"), Number(1))
    m1 = Multiply(Variable("x"), Number(9))
    l1 = LessThan(Variable("x"), Variable("y"))

    assert eval(a1.to_python)({"x": 7}) == 8
    assert eval(m1.to_python)({"x": 9}) == 81
    assert eval(l1.to_python)({"x": 7, "y": 8})
