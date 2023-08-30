from typing import Callable, Optional, TypeVar

T = TypeVar("T")


def detect(arr: list[T], func: Callable[[T], bool]) -> Optional[T]:
    # generator comprehension
    return next((i for i in arr if func(i)), None)
