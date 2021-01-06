from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from ..exceptions import Unreachable
from ..utils import detect
from .tape import Tape, TMConfiguration


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()


@dataclass
class TMRule:
    state: int
    character: str
    next_state: int
    write_character: str
    direction: Direction

    def applies_to(self, configuration: TMConfiguration) -> bool:
        return (
            self.state == configuration.state
            and self.character == configuration.tape.middle
        )

    def next_tape(self, configuration: TMConfiguration) -> Tape:
        written_tape = configuration.tape.write(self.write_character)
        if self.direction == Direction.LEFT:
            return written_tape.move_head_left
        elif self.direction == Direction.RIGHT:
            return written_tape.move_head_right
        else:
            raise Unreachable

    def follow(self, configuration: TMConfiguration) -> TMConfiguration:
        return TMConfiguration(self.next_state, self.next_tape(configuration))


@dataclass
class DTMRulebook:
    rules: List[TMRule]

    def applies_to(self, configuration: TMConfiguration):
        return self.rule_for(configuration) is not None

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

    @property
    def is_stuck(self):
        return not self.accepting and not self.rulebook.applies_to(
            self.current_configuration
        )

    def step(self):
        self.current_configuration = self.rulebook.next_configuration(
            self.current_configuration
        )

    def run(self, debug: bool = False):
        if debug:
            print(self.current_configuration)

        while True:
            if self.accepting or self.is_stuck:
                return

            self.step()
            if debug:
                print(self.current_configuration)
