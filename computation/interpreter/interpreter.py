from __future__ import print_function, unicode_literals

from expressions import Add, Multiply, LessThan, Number, Variable
from statements import Assign, Sequence, While


class Machine(object):
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression, self.environment = self.expression.reduce(
            self.environment)

    def run(self):
        while self.expression.reducible:
            print('{}, {}'.format(self.expression, self.environment))
            self.step()
        print('{}, {}'.format(self.expression, self.environment))


def test():
    SEP = '=' * 50
    seq = Assign('x', Add(Variable('x'), Number(1)))
    Machine(seq, {'x': Number(5)}).run()

    print(SEP)

    seq = Sequence(
        Assign('x', Add(
            Number(1), Number(1))), Assign('y', Multiply(
                Variable('x'), Number(2))))
    Machine(seq, {}).run()

    print(SEP)

    seq = Sequence(
        Assign('x', Add(
            Number(1), Number(1))), Assign('y', Add(
                Variable('x'), Number(1))))
    Machine(seq, {}).run()

    print(SEP)

    seq = While(
        LessThan(
            Variable('x'), Number(50)), Assign('x', Add(
                Variable('x'), Number(3))))
    Machine(seq, {'x': Number(1)}).run()

    print(SEP)

    print(seq.to_python)
    print(eval(seq.to_python)({'x': 1}))


if __name__ == '__main__':
    test()
