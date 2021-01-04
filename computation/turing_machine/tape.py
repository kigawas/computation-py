from dataclasses import dataclass
from typing import List

from ..automata.utils import detect


@dataclass
class Tape:
    left: list
    middle: str
    right: list
    blank: str

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


@dataclass
class TMRule:
    state: int
    character: str
    next_state: int
    write_character: str
    direction: str

    def applies_to(self, configuration: TMConfiguration) -> bool:
        return (
            self.state == configuration.state
            and self.character == configuration.tape.middle
        )

    def next_tape(self, configuration: TMConfiguration) -> Tape:
        written_tape = configuration.tape.write(self.write_character)
        if self.direction == "left":
            return written_tape.move_head_left
        elif self.direction == "right":
            return written_tape.move_head_right
        else:
            raise ValueError

    def follow(self, configuration: TMConfiguration) -> TMConfiguration:
        return TMConfiguration(self.next_state, self.next_tape(configuration))


@dataclass
class DTMRulebook:
    rules: List[TMRule]

    def rule_for(self, configuration: TMConfiguration):
        return detect(self.rules, lambda rule: rule.applies_to(configuration))

    def next_configuration(self, configuration: TMConfiguration):
        return self.rule_for(configuration).follow(configuration)


@dataclass
class DTM:
    current_configuration: TMConfiguration
    accept_states: list
    rulebook: DTMRulebook

    @property
    def accepting(self):
        return self.current_configuration.state in self.accept_states

    def step(self):
        self.current_configuration = self.rulebook.next_configuration(
            self.current_configuration
        )

    def run(self):
        while True:
            self.step()
            if self.accepting:
                return
