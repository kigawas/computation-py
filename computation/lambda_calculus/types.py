# Church numbers
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
TWO = lambda f: lambda x: f(f(x))
THREE = lambda f: lambda x: f(f(f(x)))
FIVE = lambda f: lambda x: f(f(f(f(f(x)))))


def to_integer(lb):
    return lb(lambda n: n + 1)(0)


# conditions
TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y
IF = lambda b: b
IS_ZERO = lambda n: n(lambda x: FALSE)(TRUE)


def to_boolean(lb):
    return IF(lb)(True)(False)


PAIR = lambda x: lambda y: lambda f: f(x)(y)
LEFT = lambda f: f(lambda x: lambda y: x)
RIGHT = lambda f: f(lambda x: lambda y: y)


INCREMENT = lambda n: lambda f: lambda x: f(n(f)(x))
SLIDE = lambda f: PAIR(RIGHT(f))(INCREMENT(RIGHT(f)))
DECREMENT = lambda n: LEFT(n(SLIDE)(PAIR(ZERO)(ZERO)))
ADD = lambda m: lambda n: n(INCREMENT)(m)
SUB = lambda m: lambda n: n(DECREMENT)(m)
MUL = lambda m: lambda n: n(ADD(m))(ZERO)
POW = lambda m: lambda n: n(MUL(m))(ONE)

FOUR = ADD(TWO)(TWO)
SEVEN = ADD(TWO)(FIVE)
TEN = MUL(TWO)(FIVE)
FIFTEEN = MUL(THREE)(FIVE)
HUNDRED = POW(TEN)(TWO)


IS_LESS_OR_EQUAL = lambda m: lambda n: IS_ZERO(SUB(m)(n))

Z_COMBINATOR = lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args)))

MOD = Z_COMBINATOR(
    lambda mod: lambda m: lambda n: IF(IS_LESS_OR_EQUAL(n)(m))(
        lambda x: mod(SUB(m)(n))(n)(x)
    )(m)
)
