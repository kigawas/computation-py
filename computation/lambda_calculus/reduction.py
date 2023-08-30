from typing import Callable, Generator

from .generics import BoolF, Endofunctor, IntF, ReductionFunctor, T
from .struct import FIRST, IS_EMPTY, REST


def to_integer(lb: Callable[[IntF], IntF]) -> int:
    return lb(lambda n: n + 1)(0)


def to_boolean(lb: Callable[[bool], BoolF]) -> bool:
    return lb(True)(False)


def to_generator(
    lb: Endofunctor, callback: ReductionFunctor[T]
) -> Generator[T, None, None]:
    while not to_boolean(IS_EMPTY(lb)):
        first = FIRST(lb)
        yield callback(first)
        lb = REST(lb)


def to_array(lb: Endofunctor, callback: ReductionFunctor[T]) -> list[T]:
    return list(to_generator(lb, callback))


def to_integer_array(lb: Endofunctor) -> list[int]:
    return to_array(lb, to_integer)
