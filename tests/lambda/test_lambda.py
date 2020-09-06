import unittest
from computation.lambda_calculus.types import (
    to_integer,
    to_boolean,
    ZERO,
    ONE,
    TWO,
    THREE,
    FOUR,
    FIVE,
    TEN,
    HUNDRED,
    IF,
    TRUE,
    FALSE,
    IS_ZERO,
    PAIR,
    LEFT,
    RIGHT,
    INCREMENT,
    DECREMENT,
    ADD,
    SUB,
    IS_LESS_OR_EQUAL,
    MOD,
)


class LambdaTest(unittest.TestCase):
    def test_lambda(self):
        self.assertEqual(to_integer(ZERO), 0)
        self.assertEqual(to_integer(ONE), 1)
        self.assertEqual(to_integer(TWO), 2)
        self.assertEqual(to_integer(THREE), 3)
        self.assertEqual(to_integer(FOUR), 4)
        self.assertEqual(to_integer(TEN), 10)
        self.assertEqual(to_integer(HUNDRED), 100)

        self.assertEqual(IF(TRUE)("happy")("sad"), "happy")
        self.assertEqual(IF(FALSE)("happy")("sad"), "sad")
        self.assertTrue(to_boolean(IS_ZERO(ZERO)))
        self.assertFalse(to_boolean(IS_ZERO(ONE)))

        my_pair = PAIR(ONE)(TWO)
        self.assertEqual(to_integer(LEFT(my_pair)), 1)
        self.assertEqual(to_integer(RIGHT(my_pair)), 2)
        self.assertEqual(to_integer(INCREMENT(ZERO)), 1)
        self.assertEqual(to_integer(INCREMENT(TWO)), 3)
        self.assertEqual(to_integer(DECREMENT(ONE)), 0)
        self.assertEqual(to_integer(DECREMENT(TWO)), 1)
        self.assertEqual(to_integer(DECREMENT(ZERO)), 0)
        self.assertEqual(to_integer(ADD(ONE)(TWO)), 3)
        self.assertEqual(to_integer(SUB(FIVE)(THREE)), 2)

        self.assertTrue(to_boolean(IS_LESS_OR_EQUAL(TWO)(TWO)))
        self.assertTrue(to_boolean(IS_LESS_OR_EQUAL(TWO)(FIVE)))
        self.assertFalse(to_boolean(IS_LESS_OR_EQUAL(HUNDRED)(FIVE)))

        self.assertEqual(to_integer(MOD(THREE)(TWO)), 1)
        self.assertEqual(to_integer(MOD(TEN)(FOUR)), 2)
        self.assertEqual(to_integer(MOD(HUNDRED)(TWO)), 0)
        self.assertEqual(to_integer(MOD(HUNDRED)(THREE)), 1)
