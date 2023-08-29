"""
Book of Changes:

Therefore there is in the Changes the Great Primal Beginning.
This generates the two primary forces.
The two primary forces generate the four images.
The four images generate the eight trigrams
"""


ZERO = lambda _: lambda x: x
ONE = lambda f: lambda x: f(x)
TRUE = lambda x: lambda _: x
FALSE = lambda _: lambda y: y
