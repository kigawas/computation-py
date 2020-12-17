from computation.interpreter.statements import Assign, If, Sequence, While, DoNothing
from computation.interpreter.expressions import (
    Add,
    Boolean,
    Multiply,
    LessThan,
    Number,
    Variable,
)
import pytest


def test_donothing():
    assert DoNothing() == DoNothing()
    assert str(DoNothing()) == "do-nothing"
    assert DoNothing() != 1


def test_assign():
    st = Assign("x", Add(Variable("x"), Number(1)))
    assert str(st) == "x = x + 1"
    en = {"x": Number(2)}
    while st.reducible:
        st, en = st.reduce(en)
    assert en["x"] == Number(3)

    st = Assign("y", Add(Variable("x"), Number(1)))
    assert eval(st.to_python)({"x": 1}) == {"x": 1, "y": 2}


def test_if_true():
    st = If(Variable("x"), Assign("y", Number(1)), Assign("y", Number(2)))
    assert str(st) == "if (x) { y = 1 } else { y = 2 }"
    en = {"x": Boolean(True)}
    while st.reducible:
        st, en = st.reduce(en)
    assert en["y"] == Number(1)
    assert en["x"] == Boolean(True)


def test_if_false():
    st = If(Variable("x"), Assign("y", Number(1)), DoNothing())
    en = {"x": Boolean(False)}
    while st.reducible:
        st, en = st.reduce(en)
    assert st == DoNothing()
    assert en["x"] == Boolean(False)


def test_sequence():
    seq = Sequence(
        Assign("x", Add(Number(1), Number(2))),
        Assign("y", Add(Variable("x"), Number(3))),
    )
    assert str(seq) == "x = 1 + 2; y = x + 3"
    en = {}
    while seq.reducible:
        seq, en = seq.reduce(en)
    assert seq == DoNothing()
    assert en["x"] == Number(3)
    st = Sequence(
        Assign("x", Add(Number(1), Number(1))),
        Assign("y", Add(Variable("x"), Number(3))),
    )
    en = st.evaluate({})
    assert en["x"] == Number(2)
    assert en["y"] == Number(5)

    st = Sequence(
        Assign("x", Add(Number(1), Number(1))),
        Assign("y", Add(Variable("x"), Number(3))),
    )
    assert eval(st.to_python)({"x": 2, "y": 1}) == {"x": 2, "y": 5}


def test_while():
    seq = While(
        LessThan(Variable("x"), Number(5)),
        Assign("x", Multiply(Variable("x"), Number(2))),
    )
    en = {"x": Number(1)}
    assert str(seq) == "while (x < 5) { x = x * 2 }"
    while seq.reducible:
        seq, en = seq.reduce(en)
    assert en["x"] == Number(8)

    st = While(
        LessThan(Variable("x"), Number(1000)),
        Assign("x", Add(Variable("x"), Number(1))),
    )
    en = st.evaluate({"x": Number(1)})
    assert en["x"] == Number(1000)

    with pytest.raises(RuntimeError):
        st.evaluate_with_recursion({"x": Number(-1000)})

    st = While(
        LessThan(Variable("x"), Number(100)),
        Assign("x", Add(Variable("x"), Number(1))),
    )
    assert eval(st.to_python)({"x": 1}) == {"x": 100}


def test_if_true_and_false():
    st = If(
        LessThan(Variable("x"), Number(5)),
        Assign("x", Number(2)),
        Assign("x", Multiply(Variable("x"), Variable("x"))),
    )
    en = st.evaluate({"x": Number(2)})
    assert en["x"] == Number(2)

    st = If(
        LessThan(Variable("x"), Number(5)),
        Assign("x", Number(2)),
        Assign("x", Multiply(Variable("x"), Variable("x"))),
    )
    en = st.evaluate({"x": Number(10)})
    assert en["x"] == Number(100)


def test_if():
    st = If(
        LessThan(Variable("x"), Number(5)),
        Assign("x", Number(2)),
        Assign("x", Multiply(Variable("x"), Variable("x"))),
    )
    assert eval(st.to_python)({"x": 1}) == {"x": 2}
