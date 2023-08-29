from dataclasses import dataclass


@dataclass
class Tape:
    left: list[str]
    middle: str
    right: list[str]
    blank: str = "_"

    def __str__(self):
        return f"<Tape: {''.join(self.left)}({self.middle}){''.join(self.right)}>"

    def write(self, character):
        return Tape(self.left, character, self.right, self.blank)

    @property
    def move_head_left(self):
        left = self.left[:-1]
        middle = self.left[-1] if self.left != [] else self.blank
        right = [self.middle] + self.right
        return Tape(left, middle, right, self.blank)

    @property
    def move_head_right(self):
        left = self.left + [self.middle]
        middle = self.right[0] if self.right != [] else self.blank
        right = self.right[1:]
        return Tape(left, middle, right, self.blank)


@dataclass
class TMConfiguration:
    state: int
    tape: Tape

    def __str__(self) -> str:
        return f"<TMConfiguration: {self.state}, {self.tape}>"
