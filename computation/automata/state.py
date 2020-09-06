from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class State:
    """
    Every state is unique
    """
