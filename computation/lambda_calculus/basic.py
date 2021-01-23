# Church numbers
# n(F) => call F n times
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
