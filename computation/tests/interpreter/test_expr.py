import unittest

from computation.interpreter.expressions import Add, Boolean, Multiply,\
    LessThan, Number, Variable


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
        n1 = Number(5)
        b1 = Boolean(False)
        v1 = Variable('x')

        self.assertEqual(eval(n1.to_python)({}), 5)
        self.assertEqual(eval(b1.to_python)({}), False)
        self.assertEqual(eval(v1.to_python)({'x': 7}), 7)

    def test_expr(self):
        a1 = Add(Variable('x'), Number(1))
        m1 = Multiply(Variable('x'), Number(9))
        l1 = LessThan(Variable('x'), Variable('y'))

        self.assertEqual(eval(a1.to_python)({'x': 7}), 8)
        self.assertEqual(eval(m1.to_python)({'x': 9}), 81)
        self.assertEqual(eval(l1.to_python)({'x': 7, 'y': 8}), True)


if __name__ == '__main__':
    unittest.main()
