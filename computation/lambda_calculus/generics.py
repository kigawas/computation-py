from typing import Callable, TypeVar

# generics
T = TypeVar("T")
IdentityF = Callable[[T], T]
IntF = IdentityF[int]
BoolF = IdentityF[bool]
Endofunctor = Callable[[Callable[[T], T]], Callable[[T], T]]  # IdentityF[IdentityF]
ReductionFunctor = Callable[
    [Callable[[Callable[[T], T]], Callable[[T], T]]], T
]  # Callable[[Endofunctor], T]
