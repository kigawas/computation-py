from computation.lambda_calculus.types import (
    ADD,
    DECREMENT,
    FALSE,
    FIVE,
    FOUR,
    HUNDRED,
    IF,
    INCREMENT,
    IS_LESS_OR_EQUAL,
    IS_ZERO,
    LEFT,
    MOD,
    ONE,
    PAIR,
    RIGHT,
    SUB,
    TEN,
    THREE,
    TRUE,
    TWO,
    ZERO,
    to_boolean,
    to_integer,
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
