from typing import Callable, List, Optional, TypeVar

T = TypeVar("T")


def detect(arr: List[T], func: Callable[[T], bool]) -> Optional[T]:
    # generator comprehension
    return next((i for i in arr if func(i)), None)
