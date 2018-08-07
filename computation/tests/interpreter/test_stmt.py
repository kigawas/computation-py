import unittest

from computation.interpreter.statements import Assign, If, Sequence, While, DoNothing
from computation.interpreter.expressions import (
    Add,
    Boolean,
    Multiply,
    LessThan,
    Number,
    Variable,
)


class StatementTest(unittest.TestCase):
    def test_donothing(self):
        self.assertEqual(DoNothing(), DoNothing())
        self.assertEqual(str(DoNothing()), "Do nothing")
        self.assertNotEqual(DoNothing(), 1)

    def test_assign(self):
        st = Assign("x", Add(Variable("x"), Number(1)))
        self.assertEqual(str(st), "x = (x + 1)")
        en = {"x": Number(2)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(en["x"], Number(3))

    def test_if_true(self):
        st = If(Variable("x"), Assign("y", Number(1)), Assign("y", Number(2)))
        self.assertEqual(str(st), "if (x) { y = 1 } else { y = 2 }")
        en = {"x": Boolean(True)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(en["y"], Number(1))
        self.assertEqual(en["x"], Boolean(True))

    def test_if_false(self):
        st = If(Variable("x"), Assign("y", Number(1)), DoNothing())
        en = {"x": Boolean(False)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(st, DoNothing())
        self.assertEqual(en["x"], Boolean(False))

    def test_sequence(self):
        seq = Sequence(
            Assign("x", Add(Number(1), Number(2))),
            Assign("y", Add(Variable("x"), Number(3))),
        )
        self.assertEqual(str(seq), "x = (1 + 2); y = (x + 3)")
        en = {}
        while seq.reducible:
            seq, en = seq.reduce(en)
        self.assertEqual(seq, DoNothing())
        self.assertEqual(en["x"], Number(3))

    def test_while(self):
        seq = While(
            LessThan(Variable("x"), Number(5)),
            Assign("x", Multiply(Variable("x"), Number(2))),
        )
        en = {"x": Number(1)}
        self.assertEqual(str(seq), "while (x < 5) { x = (x * 2) }")
        while seq.reducible:
            seq, en = seq.reduce(en)
        self.assertEqual(en["x"], Number(8))


class EvalTest(unittest.TestCase):
    def test_sequence(self):
        st = Sequence(
            Assign("x", Add(Number(1), Number(1))),
            Assign("y", Add(Variable("x"), Number(3))),
        )
        en = st.evaluate({})
        self.assertEqual(en["x"], Number(2))
        self.assertEqual(en["y"], Number(5))

    def test_if_true_and_false(self):
        st = If(
            LessThan(Variable("x"), Number(5)),
            Assign("x", Number(2)),
            Assign("x", Multiply(Variable("x"), Variable("x"))),
        )
        en = st.evaluate({"x": Number(2)})
        self.assertEqual(en["x"], Number(2))

        st = If(
            LessThan(Variable("x"), Number(5)),
            Assign("x", Number(2)),
            Assign("x", Multiply(Variable("x"), Variable("x"))),
        )
        en = st.evaluate({"x": Number(10)})
        self.assertEqual(en["x"], Number(100))

    def test_while(self):
        st = While(
            LessThan(Variable("x"), Number(1000)),
            Assign("x", Add(Variable("x"), Number(1))),
        )
        en = st.evaluate({"x": Number(1)})
        self.assertEqual(en["x"], Number(1000))

        with self.assertRaises(RuntimeError):
            st.evaluate_with_recursion({"x": Number(-1000)})


class CodeGenTest(unittest.TestCase):
    def test_assign(self):
        st = Assign("y", Add(Variable("x"), Number(1)))
        self.assertEqual(eval(st.to_python)({"x": 1}), {"x": 1, "y": 2})

    def test_if(self):
        st = If(
            LessThan(Variable("x"), Number(5)),
            Assign("x", Number(2)),
            Assign("x", Multiply(Variable("x"), Variable("x"))),
        )
        self.assertEqual(eval(st.to_python)({"x": 1}), {"x": 2})

    def test_sequence(self):
        st = Sequence(
            Assign("x", Add(Number(1), Number(1))),
            Assign("y", Add(Variable("x"), Number(3))),
        )
        self.assertEqual(eval(st.to_python)({"x": 2, "y": 1}), {"x": 2, "y": 5})

    def test_while(self):
        st = While(
            LessThan(Variable("x"), Number(100)),
            Assign("x", Add(Variable("x"), Number(1))),
        )
        self.assertEqual(eval(st.to_python)({"x": 1}), {"x": 100})
