from __future__ import print_function, unicode_literals

from expressions import Add, Boolean, Multiply, LessThan, Number, Variable
from statements import Assign, If, Sequence

class Machine(object):
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression, self.environment = self.expression.reduce(self.environment)

    def run(self):
        while self.expression.reducible:
            print("{}, {}".format(self.expression, self.environment))
            self.step()
        print("{}, {}".format(self.expression, self.environment))


def test():

    expr = Assign('x', Add(Variable('x'), Number(1)))

    #Machine(expr, {'x': Number(5)}).run()
    seq = Sequence(
        Assign('x', Add(
            Number(1), Number(1))), Assign('y', Add(
                Variable('x'), Number(3))))
    Machine(seq,{}).run()


if __name__ == '__main__':
    test()
