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


def test_lambda():
    assert to_integer(ZERO) == 0
    assert to_integer(ONE) == 1
    assert to_integer(TWO) == 2
    assert to_integer(THREE) == 3
    assert to_integer(FOUR) == 4
    assert to_integer(TEN) == 10
    assert to_integer(HUNDRED) == 100

    assert IF(TRUE)("happy")("sad") == "happy"
    assert IF(FALSE)("happy")("sad") == "sad"
    assert to_boolean(IS_ZERO(ZERO))
    assert not (to_boolean(IS_ZERO(ONE)))

    my_pair = PAIR(ONE)(TWO)
    assert to_integer(LEFT(my_pair)) == 1
    assert to_integer(RIGHT(my_pair)) == 2
    assert to_integer(INCREMENT(ZERO)) == 1
    assert to_integer(INCREMENT(TWO)) == 3
    assert to_integer(DECREMENT(ONE)) == 0
    assert to_integer(DECREMENT(TWO)) == 1
    assert to_integer(DECREMENT(ZERO)) == 0
    assert to_integer(ADD(ONE)(TWO)) == 3
    assert to_integer(SUB(FIVE)(THREE)) == 2

    assert to_boolean(IS_LESS_OR_EQUAL(TWO)(TWO))
    assert to_boolean(IS_LESS_OR_EQUAL(TWO)(FIVE))
    assert not (to_boolean(IS_LESS_OR_EQUAL(HUNDRED)(FIVE)))

    assert to_integer(MOD(THREE)(TWO)) == 1
    assert to_integer(MOD(TEN)(FOUR)) == 2
    assert to_integer(MOD(HUNDRED)(TWO)) == 0
    assert to_integer(MOD(HUNDRED)(THREE)) == 1
