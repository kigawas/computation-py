from itertools import islice
from typing import Callable, Generator, List, TypeVar

from computation.lambda_calculus import (
    ADD,
    CLOSED_RANGE,
    DECREMENT,
    EMPTY,
    FALSE,
    FIRST,
    FIVE,
    FOLD,
    FOUR,
    HUNDRED,
    IF,
    INCREMENT,
    IS_EMPTY,
    IS_LESS_OR_EQUAL,
    IS_ZERO,
    LEFT,
    MAP,
    MOD,
    MUL,
    MULTIPLES_OF,
    NOT,
    ONE,
    PAIR,
    RANGE,
    REST,
    RIGHT,
    SUB,
    TEN,
    THREE,
    TRUE,
    TWO,
    UNSHIFT,
    UPWARDS_OF,
    ZERO,
    ZEROS,
    to_boolean,
    to_generator,
    to_integer,
    to_integer_array,
)

T = TypeVar("T")
U = TypeVar("U")


def mod(m: int, n: int) -> int:
    return mod(m - n, n) if m >= n else m


def range_(m: int, n: int):
    # [m, n)
    return [m] + range_(m + 1, n) if m < n else []


def fold(arr: List[T], init: U, func: Callable[[T, U], U]) -> U:
    return func(arr[0], fold(arr[1:], init, func)) if arr else init


def map_(arr: List[T], func: Callable[[T], T]) -> List[T]:
    return fold(arr, [], lambda x, l: [func(x)] + l)


def unshift(gen: Generator[int, None, None], x: int):
    yield x
    yield from gen


def zeros():
    yield from unshift(zeros(), 0)


def upwards_of(n: int):
    yield from unshift(upwards_of(n + 1), n)


def multiples_of(m: int):
    def g(n: int):
        yield from unshift(g(n + m), n)

    return g(m)


def test_algorithms():
    assert mod(5, 3) == 2
    assert mod(15, 4) == 3
    assert range_(1, 3) == [1, 2]
    assert fold([1, 2, 3, 4, 5], 0, lambda x, y: x + y) == 15
    assert fold([1, 2, 3, 4, 5], 1, lambda x, y: x * y) == 120
    assert map_([], lambda _: 0) == []
    assert map_([1, 2, 3], lambda x: x + 1) == [2, 3, 4]
    assert list(islice(zeros(), 100)) == [0] * 100
    assert list(islice(upwards_of(5), 100)) == list(range(5, 105))
    assert list(islice(multiples_of(5), 3)) == [5, 10, 15]


def test_number():
    assert to_integer(ZERO) == 0
    assert to_integer(ONE) == 1
    assert to_integer(TWO) == 2
    assert to_integer(THREE) == 3
    assert to_integer(FOUR) == 4
    assert to_integer(TEN) == 10
    assert to_integer(HUNDRED) == 100


def test_cond():
    assert IF(TRUE)("happy")("sad") == "happy"
    assert IF(FALSE)("happy")("sad") == "sad"
    assert TRUE("happy")("sad") == "happy"
    assert FALSE("happy")("sad") == "sad"
    assert to_boolean(IS_ZERO(ZERO))
    assert not to_boolean(IS_ZERO(ONE))
    assert not to_boolean(NOT(IS_ZERO(ZERO)))
    assert to_boolean(NOT(IS_ZERO(ONE)))


def test_calc():
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
    assert to_integer(SUB(THREE)(FIVE)) == 0

    assert to_boolean(IS_LESS_OR_EQUAL(TWO)(TWO))
    assert to_boolean(IS_LESS_OR_EQUAL(TWO)(FIVE))
    assert not (to_boolean(IS_LESS_OR_EQUAL(HUNDRED)(FIVE)))

    assert to_integer(MOD(THREE)(TWO)) == 1
    assert to_integer(MOD(TEN)(FOUR)) == 2
    assert to_integer(MOD(HUNDRED)(TWO)) == 0
    assert to_integer(MOD(HUNDRED)(THREE)) == 1


def test_list():
    my_list = UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(THREE))(TWO))(ONE)

    assert to_integer(FIRST(my_list)) == 1
    assert to_integer(FIRST(REST(my_list))) == 2
    assert to_integer(FIRST(REST(REST(my_list)))) == 3
    assert to_boolean(IS_EMPTY(EMPTY))
    assert not to_boolean(IS_EMPTY(my_list))

    assert to_integer_array(my_list) == [1, 2, 3]
    assert to_integer_array(RANGE(ONE)(FOUR)) == [1, 2, 3]
    assert to_integer_array(CLOSED_RANGE(ONE)(THREE)) == [1, 2, 3]


def test_higher_order_func():
    assert to_integer(FOLD(CLOSED_RANGE(ONE)(FIVE))(ZERO)(ADD)) == 15
    assert to_integer(FOLD(CLOSED_RANGE(ONE)(FIVE))(ONE)(MUL)) == 120

    one_to_three = MAP(RANGE(ZERO)(THREE))(INCREMENT)
    assert to_integer_array(one_to_three) == [1, 2, 3]


def test_streams():
    def test_gen(n: int):
        assert list(islice(to_generator(ZEROS, to_integer), n)) == [0] * n
        assert list(islice(to_generator(UPWARDS_OF(FIVE), to_integer), n)) == list(
            range(5, 5 + n)
        )
        assert list(islice(to_generator(MULTIPLES_OF(TWO), to_integer), n)) == list(
            range(2, 2 * n + 2, 2)
        )

    test_gen(0)
    test_gen(1)
    test_gen(10)
    test_gen(100)
