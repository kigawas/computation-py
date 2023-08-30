from .basic import FALSE, TRUE
from .calculation import SUB

IF = lambda b: b  # reduced from `lambda b: lambda x: lambda y: b(x)(y)`
NOT = lambda b: b(FALSE)(TRUE)

IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
IS_LESS_OR_EQUAL = lambda m: lambda n: IS_ZERO(SUB(m)(n))
IS_LESS = lambda m: lambda n: NOT(IS_LESS_OR_EQUAL(n)(m))
