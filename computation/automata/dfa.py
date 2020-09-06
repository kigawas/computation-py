from typing import List
from dataclasses import dataclass

from .farule import DFARulebook


@dataclass
class DFA:
    current_state: int
    accept_states: List[int]
    rulebook: DFARulebook

    @property
    def accepting(self) -> bool:
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)
        return self

    def read_string(self, string):
        for c in string:
            self.read_character(c)
        return self


@dataclass
class DFADesign:
    start_state: int
    accept_states: List[int]
    rulebook: DFARulebook

    @property
    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_dfa.read_string(string).accepting
