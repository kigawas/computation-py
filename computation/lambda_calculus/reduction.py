from typing import Callable, Generator, List

from .generics import IntF, BoolF, Endofunctor, ReductionFunctor, T
from .struct import IS_EMPTY, FIRST, REST


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


def to_array(lb: Endofunctor, callback: ReductionFunctor[T]) -> List[T]:
    return list(to_generator(lb, callback))


def to_integer_array(lb: Endofunctor) -> List[int]:
    return to_array(lb, to_integer)
