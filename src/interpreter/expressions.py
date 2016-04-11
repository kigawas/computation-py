from __future__ import print_function, unicode_literals

from functools import total_ordering

import unittest


@total_ordering
class Number(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Number({})'.format(self.value)

    def __str__(self):
        return '{}'.format(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    @property
    def reducible(self):
        return False


class Boolean(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Boolean({})'.format(self.value)

    def __str__(self):
        return '{}'.format(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    @property
    def reducible(self):
        return False


class Add(object):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return '({} + {})'.format(self.left, self.right)

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
        return '({} * {})'.format(self.left, self.right)

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
        return '({} < {})'.format(self.left, self.right)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible:
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible:
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)


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


class TypeTest(unittest.TestCase):
    def test_number(self):
        self.assertEqual(Number(3), Number(3))
        self.assertNotEqual(Number(3), Number(4))
        self.assertLess(Number(2), Number(4))
        self.assertGreater(Number(4), Number(2))

    def test_boolean(self):
        self.assertTrue(Boolean(True) and Boolean(True))
        self.assertEqual(Boolean(True), Boolean(True))
        self.assertEqual(Boolean(False), Boolean(False))
        self.assertNotEqual(Boolean(True), Boolean(False))


class ExprTest(unittest.TestCase):
    def test_add(self):
        expr = Add(Variable('x'), Variable('y'))
        en = {'x': Number(1), 'y': Number(2)}
        while expr.reducible:
            expr = expr.reduce(en)
        self.assertEqual(expr, Number(3))

    def test_mul(self):
        expr = Multiply(Variable('x'), Variable('y'))
        en = {'x': Number(3), 'y': Number(4)}
        while expr.reducible:
            expr = expr.reduce(en)
        self.assertEqual(expr, Number(12))

    def test_less(self):
        expr = LessThan(Variable('x'), Variable('y'))
        en = {'x': Number(1), 'y': Number(3)}
        while expr.reducible:
            expr = expr.reduce(en)
        self.assertEqual(expr, Boolean(True))


if __name__ == '__main__':
    unittest.main()
