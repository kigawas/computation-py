from dataclasses import dataclass

from .farule import FARule, DFARulebook, NFARulebook
from .dfa import DFADesign


@dataclass
class NFA:
    def __init__(self, current_states, accept_states, rulebook):
        self._current_states = frozenset(current_states)
        self.accept_states = frozenset(accept_states)
        self.rulebook = rulebook

    @property
    def current_states(self):
        return self.rulebook.follow_free_moves(self._current_states)

    @property
    def accepting(self):
        return not frozenset.isdisjoint(self.current_states, self.accept_states)

    def read_character(self, character):
        self._current_states = self.rulebook.next_states(self.current_states, character)
        return self

    def read_string(self, string):
        for c in string:
            self.read_character(c)
        return self


@dataclass
class NFADesign:
    start_state: int
    accept_states: list
    rulebook: NFARulebook

    @property
    def to_nfa(self):
        return NFA([self.start_state], self.accept_states, self.rulebook)

    def to_nfa_from(self, current_states):
        return NFA(current_states, self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_nfa.read_string(string).accepting


@dataclass
class NFASimulation:
    nfa_design: NFADesign

    def next_state(self, state, character):
        return (
            self.nfa_design.to_nfa_from(set(state))
            .read_character(character)
            .current_states
        )

    def rules_for(self, state):
        return [
            FARule(set(state), character, self.next_state(state, character))
            for character in self.nfa_design.rulebook.alphabet
        ]

    def discover_states_and_rules(self, states):
        states = [frozenset(state) for state in states]
        rules = sum([self.rules_for(state) for state in states], [])
        more_states = frozenset([frozenset(rule.follow) for rule in rules])

        if more_states.issubset(states):
            return states, rules
        else:
            return self.discover_states_and_rules(more_states.union(states))

    @property
    def to_dfa_design(self):
        start_state = self.nfa_design.to_nfa.current_states
        states, rules = self.discover_states_and_rules([start_state])
        accept_states = [
            state for state in states if self.nfa_design.to_nfa_from(state).accepting
        ]
        return DFADesign(start_state, accept_states, DFARulebook(rules))
