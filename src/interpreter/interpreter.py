from __future__ import print_function, unicode_literals

from expressions import Add, Boolean, Multiply, LessThan, Number, Variable
from statements import Assign, If, Sequence, While
from utils import merge_dict


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
    expr = Assign('x', Add(Variable('x'), Number(1)))
    Machine(expr, {'x': Number(5)}).run()

    seq = Sequence(
        Assign('x', Add(
            Number(1), Number(1))), Assign('y', Add(
                Variable('x'), Number(1))))
    Machine(seq, {}).run()

    seq = While(
        LessThan(
            Variable('x'), Number(50)), Assign('x', Add(
                Variable('x'), Number(3))))
    Machine(seq, {'x': Number(1)}).run()
    print(seq.to_python)
    print(eval(seq.to_python)({'x': 1}))


if __name__ == '__main__':
    test()
