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
        return 'if ({}) \{ {} \} else \{ {} \}'.format(self.condition, self.consequence, self.alternative)

    @property
    def reducible(self):
        return True

    def reduce(self, environment):
        if self.condition.reducible:
            return If(self.condition.reduce(environment), self.consequence, self.alternative), environment
        else:
            if self.condition == Boolean(True):
                return self.consequence, environment
            elif self.condition == Boolean(False):
                return self.alternative, environment
            else:
                pass

class TestStatements(unittest.TestCase):
    def test_donothing(self):
        self.assertEqual(DoNothing(), DoNothing())
        self.assertNotEqual(DoNothing(), 1)

    def test_assign(self):
        st = Assign('x', Add(Variable('x'), Number(1)))
        en = {'x': Number(2)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(en['x'], Number(3))

    def test_if(self):
        st = If(Variable('x'), Assign('y', Number(1)), Assign('y', Number(2)))
        en = {'x': Boolean(True)}
        while st.reducible:
            st, en = st.reduce(en)
        self.assertEqual(en['y'], Number(1))
        self.assertEqual(en['x'], Boolean(True))


if __name__ == '__main__':
    unittest.main()
