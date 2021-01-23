from .basic import ONE, ZERO, IS_ZERO, NOT, TWO, FIVE, THREE

from .struct import PAIR, RIGHT, LEFT

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
