from __future__ import print_function, unicode_literals
import unittest

from  expressions  import *

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


class EvalTest(unittest.TestCase):
    def test_type(self):
        self.assertEqual(Number(23).evaluate({}), Number(23))
        self.assertEqual(Variable('x').evaluate({'x': Number(23)}), Number(23))
        self.assertEqual(
            LessThan(
                Add(
                    Variable('x'), Number(2)),
                Variable('y')).evaluate({'x': Number(2),
                                         'y': Number(5)}), Boolean(True))


class CodeGenTest(unittest.TestCase):
    def test_type(self):
        n1 = Number(5).to_python
        b1 = Boolean(False).to_python
        v1 = Variable('x').to_python

        self.assertEqual(eval(n1)({}), 5)
        self.assertEqual(eval(b1)({}), False)
        self.assertEqual(eval(v1)({'x': 7}), 7)

    def test_expr(self):
        a1 = Add(Variable('x'), Number(1)).to_python
        m1 = Multiply(Variable('x'), Number(9)).to_python
        l1 = LessThan(Variable('x'), Variable('y')).to_python

        self.assertEqual(eval(a1)({'x': 7}), 8)
        self.assertEqual(eval(m1)({'x': 9}), 81)
        self.assertEqual(eval(l1)({'x': 7, 'y': 8}), True)


if __name__ == '__main__':
    unittest.main()
