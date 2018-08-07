from dataclasses import dataclass


@dataclass
class FARule:
    state: int
    character: str
    next_state: int

    def __repr__(self) -> str:
        return f"FARule({self.state}, {self.character}, {self.next_state})"

    def __str__(self) -> str:
        return f"#<FARule {self.state} --{self.character}--> {self.next_state}"

    def applies_to(self, state, character) -> bool:
        return self.state == state and self.character == character

    @property
    def follow(self):
        return self.next_state

    def reverse(self):
        return FARule(self.next_state, self.character, self.state)
