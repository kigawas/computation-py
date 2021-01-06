from dataclasses import dataclass
from typing import List

from ..utils import detect
from .tape import TMConfiguration, Tape


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

    def run(self, debug: bool = False):
        if debug:
            print(self.current_configuration)

        while True:
            if self.accepting:
                return

            self.step()
            if debug:
                print(self.current_configuration)
