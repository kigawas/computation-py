from typing import Any, Callable, Generator, List, TypeVar

T = TypeVar("T")
IdentityF = Callable[[T], T]


# Church numbers
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
TWO = lambda f: lambda x: f(f(x))
THREE = lambda f: lambda x: f(f(f(x)))
FIVE = lambda f: lambda x: f(f(f(f(f(x)))))


# conditions
TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y
IF = lambda b: b  # reduced from `lambda b: lambda x: lambda y: b(x)(y)`
NOT = lambda b: b(FALSE)(TRUE)
IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)


# pair
PAIR = lambda x: lambda y: lambda f: f(x)(y)
LEFT = lambda f: f(lambda x: lambda y: x)
RIGHT = lambda f: f(lambda x: lambda y: y)

# calculation
INCREMENT = lambda n: lambda f: lambda x: f(n(f)(x))
SLIDE = lambda f: PAIR(RIGHT(f))(INCREMENT(RIGHT(f)))
DECREMENT = lambda n: LEFT(n(SLIDE)(PAIR(ZERO)(ZERO)))
ADD = lambda m: lambda n: n(INCREMENT)(m)
SUB = lambda m: lambda n: n(DECREMENT)(m)
MUL = lambda m: lambda n: n(ADD(m))(ZERO)
POW = lambda m: lambda n: n(MUL(m))(ONE)
IS_LESS_OR_EQUAL = lambda m: lambda n: IS_ZERO(SUB(m)(n))
IS_LESS = lambda m: lambda n: NOT(IS_LESS_OR_EQUAL(n)(m))

# more numbers
FOUR = ADD(TWO)(TWO)
SEVEN = ADD(TWO)(FIVE)
TEN = MUL(TWO)(FIVE)
FIFTEEN = MUL(THREE)(FIVE)
HUNDRED = POW(TEN)(TWO)

# Y combinator equiv
Z_COMBINATOR = lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args)))

# list
EMPTY = PAIR(TRUE)(TRUE)
UNSHIFT = lambda l: lambda x: PAIR(FALSE)(PAIR(x)(l))
IS_EMPTY = LEFT
FIRST = lambda l: LEFT(RIGHT(l))
REST = lambda l: RIGHT(RIGHT(l))

# recursive algorithms, see equivalent python code in test_lambda.py
MOD = Z_COMBINATOR(
    lambda mod: lambda m: lambda n: IF(IS_LESS_OR_EQUAL(n)(m))(
        lambda *args: mod(SUB(m)(n))(n)(*args)
    )(m)
)

RANGE = Z_COMBINATOR(
    lambda range: lambda m: lambda n: IF(IS_LESS(m)(n))(
        lambda *args: UNSHIFT(range(INCREMENT(m))(n))(m)(*args)
    )(EMPTY)
)
CLOSED_RANGE = lambda m: lambda n: RANGE(m)(INCREMENT(n))

FOLD = Z_COMBINATOR(
    lambda fold: lambda l: lambda init: lambda func: IF(IS_EMPTY(l))(init)(
        lambda *args: func(FIRST(l))(fold(REST(l))(init)(func))(*args)
    )
)

MAP = lambda l: lambda func: FOLD(l)(EMPTY)(
    lambda x: lambda result: UNSHIFT(result)(func(x))
)

# streams, see equivalent python code in test_lambda.py
ZEROS = Z_COMBINATOR(lambda zeros: UNSHIFT(zeros)(ZERO))
UPWARDS_OF = Z_COMBINATOR(
    lambda upwards: lambda n: UNSHIFT(lambda *args: upwards(INCREMENT(n))(*args))(n)
)
MULTIPLES_OF = lambda m: Z_COMBINATOR(
    lambda multiples: lambda n: UNSHIFT(lambda *args: multiples(ADD(m)(n))(*args))(n)
)(m)


def to_integer(lb: Callable[[IdentityF], IdentityF]) -> int:
    return lb(lambda n: n + 1)(0)


def to_boolean(lb: Callable[[bool], IdentityF]) -> bool:
    return lb(True)(False)


def to_generator(
    lb: Callable, callback: Callable[[Any], T]
) -> Generator[T, None, None]:
    while True:
        if to_boolean(IS_EMPTY(lb)):
            break

        yield callback(FIRST(lb))
        lb = REST(lb)


def to_array(lb: Callable, callback: Callable[[Any], T]) -> List[T]:
    return list(to_generator(lb, callback))


def to_integer_array(lb: Callable) -> List[int]:
    return to_array(lb, to_integer)
