from __future__ import print_function

from utils import merge_dict




class Number(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{}".format(self.value)

    @property
    def reducible(self):
        return False

class Boolean(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{}".format(self.value)

    @property
    def reducible(self):
        return False

class Add(object):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return "({} + {})".format(self.left, self.right)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return Add(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)


class Multiply(object):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return "({} * {})".format(self.left, self.right)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)

class LessThan(object):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return "({} < {})".format(self.left, self.right)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.left.value)


class Variable(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{}".format(self.name)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]
        
class Machine(object):
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression = self.expression.reduce(self.environment)

    def run(self):
        while self.expression.reducible:
            print(self.expression)
            self.step()
        print(self.expression)


def test():
    # expr1 = Add(Multiply(Number(1), Number(2)), Multiply(Number(3), Number(4)))
    # Machine(expr1).run()
    #
    # expr2 = Multiply(Number(1), Multiply(Add(Number(2), Number(3)), Number(4)))
    # Machine(expr2).run()

    expr3 = LessThan(Variable('x'), Add(Variable('y'), Variable('y')))
    Machine(expr3, {'x':Number(5),'y':Number(2)}).run()


if __name__ == '__main__':
    test()
