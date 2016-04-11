from __future__ import print_function, unicode_literals

import unittest

from expressions import Variable, Add, Number, Boolean
from utils import merge_dict


class DoNothing(object):
    def __str__(self):
        return 'Do nothing'

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    @property
    def reducible(self):
        return False


class Assign(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return '{} = {}'.format(self.name, self.expression)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.expression.reducible:
            return Assign(self.name,
                          self.expression.reduce(environment)), environment
        else:
            return DoNothing(), merge_dict(environment, {self.name:
                                                         self.expression})


class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return 'if ({}) \{ {} \} else \{ {} \}'.format(
            self.condition, self.consequence, self.alternative)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.condition.reducible:
            return If(
                self.condition.reduce(environment), self.consequence,
                self.alternative), environment
        else:
            if self.condition == Boolean(True):
                return self.consequence, environment
            elif self.condition == Boolean(False):
                return self.alternative, environment
            else:
                pass


class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return '{}; {}'.format(self.first, self.second)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.first == DoNothing():
            return self.second, environment
        else:
            reduced_first, reduced_env = self.first.reduce(environment)
            return Sequence(reduced_first, self.second), reduced_env


class StatementTest(unittest.TestCase):
    def test_donothing(self):
        self.assertEqual(DoNothing(), DoNothing())
        self.assertNotEqual(DoNothing(), 1)

    def test_assign(self):
        st = Assign('x', Add(Variable('x'), Number(1)))
        en = {'x': Number(2)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(en['x'], Number(3))

    def test_if_true(self):
        st = If(Variable('x'), Assign('y', Number(1)), Assign('y', Number(2)))
        en = {'x': Boolean(True)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(en['y'], Number(1))
        self.assertEqual(en['x'], Boolean(True))

    def test_if_false(self):
        st = If(Variable('x'), Assign('y', Number(1)), DoNothing())
        en = {'x': Boolean(False)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(st, DoNothing())
        self.assertEqual(en['x'], Boolean(False))

    def test_sequence(self):
        seq = Sequence(
            Assign('x', Add(
                Number(1), Number(2))), Assign('y', Add(
                    Variable('x'), Number(3))))
        en = {}
        while seq.reducible:
            seq, en = seq.reduce(en)
        self.assertEqual(seq, DoNothing())
        self.assertEqual(en['x'], Number(3))


if __name__ == '__main__':
    unittest.main()
