from .basic import IF
from .calc import SUB, IS_LESS_OR_EQUAL, IS_LESS, INCREMENT
from .struct import UNSHIFT, FIRST, EMPTY, REST, IS_EMPTY

# Y combinator equiv
Z_COMBINATOR = lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args)))


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
