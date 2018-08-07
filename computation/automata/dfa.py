from dataclasses import dataclass

from computation.automata.utils import detect


@dataclass
class DFARulebook:
    rules: list

    def next_state(self, state, character):
        return self.rule_for(state, character).follow

    def rule_for(self, state, character):
        return detect(self.rules, lambda rule: rule.applies_to(state, character))


@dataclass
class DFA:
    current_state: int
    accept_states: list
    rulebook: DFARulebook

    @property
    def accepting(self):
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
    accept_states: list
    rulebook: DFARulebook

    @property
    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_dfa.read_string(string).accepting
