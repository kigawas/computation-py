from .basic import FALSE, TRUE

# pair
PAIR = lambda x: lambda y: lambda f: f(x)(y)
LEFT = lambda f: f(lambda x: lambda _: x)
RIGHT = lambda f: f(lambda _: lambda y: y)
IS_EMPTY = LEFT

# list
EMPTY = PAIR(TRUE)(TRUE)
UNSHIFT = lambda l: lambda x: PAIR(FALSE)(PAIR(x)(l))  # Add x to front
FIRST = lambda l: LEFT(RIGHT(l))
REST = lambda l: RIGHT(RIGHT(l))
