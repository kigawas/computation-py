import os
import sys

sys.path.append(os.path.realpath('.'))

from computation.interpreter.interpreter import Machine
from computation.interpreter.expressions import Add, Variable, Number, Multiply, LessThan
from computation.interpreter.statements import Sequence, Assign, While


def test_interpreter():
    SEP = '=' * 50
    seq = Assign('x', Add(Variable('x'), Number(1)))
    Machine(seq, {'x': Number(5)}).run()

    print(SEP)

    seq = Sequence(
        Assign('x', Add(
            Number(1), Number(1))), Assign('y', Multiply(
                Variable('x'), Number(2))))  # NOQA
    Machine(seq, {}).run()

    print(SEP)

    seq = Sequence(
        Assign('x', Add(
            Number(1), Number(1))), Assign('y', Add(
                Variable('x'), Number(1))))  # NOQA
    Machine(seq, {}).run()

    print(SEP)

    seq = While(
        LessThan(
            Variable('x'), Number(50)), Assign('x', Add(
                Variable('x'), Number(3))))  # NOQA
    Machine(seq, {'x': Number(1)}).run()

    print(SEP)

    print(seq.to_python)
    print(eval(seq.to_python)({'x': 1}))

if __name__ == '__main__':
    test_interpreter()
