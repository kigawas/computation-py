import unittest

from computation.interpreter.interpreter import Machine
from computation.interpreter.expressions import (
    Add,
    Variable,
    Number,
    Multiply,
    LessThan,
)
from computation.interpreter.statements import Sequence, Assign, While


class InterpreterTest(unittest.TestCase):
    def test_interpreter(self):
        SEP = "=" * 50
        seq = Assign("x", Add(Variable("x"), Number(1)))
        Machine(seq, {"x": Number(5)}, True).run()

        print(SEP)

        seq = Sequence(
            Assign("x", Add(Number(1), Number(1))),
            Assign("y", Multiply(Variable("x"), Number(2))),
        )
        Machine(seq, {}, True).run()

        print(SEP)

        seq = Sequence(
            Assign("x", Add(Number(1), Number(1))),
            Assign("y", Add(Variable("x"), Number(1))),
        )
        Machine(seq, {}, True).run()

        print(SEP)

        seq = While(
            LessThan(Variable("x"), Number(50)),
            Assign("x", Add(Variable("x"), Number(3))),
        )
        Machine(seq, {"x": Number(1)}).run()

        self.assertEqual(eval(seq.to_python)({"x": 1}), {"x": 52})
