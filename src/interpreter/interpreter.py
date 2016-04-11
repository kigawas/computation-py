from __future__ import print_function, unicode_literals

from expressions import Add, Boolean, Multiply, LessThan, Number, Variable
from statements import Assign

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
    Machine(expr, {'x': Number(5)}).run()


if __name__ == '__main__':
    test()
