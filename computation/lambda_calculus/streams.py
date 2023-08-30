from .basic import ZERO
from .calculation import ADD, INCREMENT
from .func import Z_COMBINATOR
from .struct import UNSHIFT

# streams, see equivalent python code in test_lambda.py
ZEROS = Z_COMBINATOR(lambda zeros: UNSHIFT(zeros)(ZERO))
UPWARDS_OF = Z_COMBINATOR(
    lambda upwards: lambda n: UNSHIFT(lambda *args: upwards(INCREMENT(n))(*args))(n)
)
MULTIPLES_OF = lambda m: Z_COMBINATOR(
    lambda multiples: lambda n: UNSHIFT(lambda *args: multiples(ADD(m)(n))(*args))(n)
)(m)
