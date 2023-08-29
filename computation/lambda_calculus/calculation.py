from .basic import ONE, ZERO
from .struct import LEFT, PAIR, RIGHT

INCREMENT = lambda n: lambda f: lambda x: f(n(f)(x))
SLIDE = lambda f: PAIR(RIGHT(f))(INCREMENT(RIGHT(f)))  # (a, b) -> (b, b+1)
DECREMENT = lambda n: LEFT(n(SLIDE)(PAIR(ZERO)(ZERO)))
ADD = lambda m: lambda n: n(INCREMENT)(m)
SUB = lambda m: lambda n: n(DECREMENT)(m)
MUL = lambda m: lambda n: n(ADD(m))(ZERO)
POW = lambda m: lambda n: n(MUL(m))(ONE)
