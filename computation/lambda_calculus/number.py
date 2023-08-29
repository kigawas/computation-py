from .basic import ONE
from .calculation import ADD, INCREMENT, MUL, POW

# Church numbers
# n(F) means call F n times, e.g. THREE(F) = F(F(F(x)))
TWO = INCREMENT(ONE)  # == lambda f: lambda x: f(f(x))
THREE = INCREMENT(TWO)  # == lambda f: lambda x: f(f(f(x)))
FOUR = ADD(TWO)(TWO)
FIVE = INCREMENT(FOUR)
SEVEN = ADD(TWO)(FIVE)
TEN = MUL(TWO)(FIVE)
FIFTEEN = MUL(THREE)(FIVE)
HUNDRED = POW(TEN)(TWO)
