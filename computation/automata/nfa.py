from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from .dfa import DFADesign
from .farule import DFARulebook, FARule, NFARulebook, State


@dataclass
class NFA:
    def __init__(
        self,
        current_states: Iterable[State],
        accept_states: Iterable[State],
        rulebook: NFARulebook,
    ):
        self.current_states = rulebook.follow_free_moves(frozenset(current_states))
        self.accept_states = frozenset(accept_states)
        self.rulebook = rulebook

    @property
    def accepting(self):
        return not frozenset.isdisjoint(self.current_states, self.accept_states)

    def read_character(self, character: Optional[str]) -> NFA:
        next_states = self.rulebook.next_states(self.current_states, character)
        self.current_states = self.rulebook.follow_free_moves(next_states)
        return self

    def read_string(self, string: str) -> NFA:
        for c in string:
            self.read_character(c)
        return self


@dataclass
class NFADesign:
    start_state: State
    accept_states: List[State]
    rulebook: NFARulebook

    @property
    def to_nfa(self) -> NFA:
        return NFA([self.start_state], self.accept_states, self.rulebook)

    def to_nfa_from(self, current_states: Iterable[State]) -> NFA:
        return NFA(current_states, self.accept_states, self.rulebook)

    def accepts(self, string: str):
        return self.to_nfa.read_string(string).accepting


@dataclass
class NFASimulation:
    nfa_design: NFADesign

    def next_state(self, state: Iterable[State], character: Optional[str]):
        return (
            self.nfa_design.to_nfa_from(set(state))
            .read_character(character)
            .current_states
        )

    def rules_for(self, state: Iterable[State]) -> List[FARule]:
        alphabet = self.nfa_design.rulebook.alphabet
        return [
            FARule(frozenset(state), character, self.next_state(state, character))
            for character in alphabet
        ]

    def discover_states_and_rules(
        self, states: frozenset
    ) -> Tuple[Iterable[Iterable[State]], List[FARule]]:
        rules_list = [self.rules_for(state) for state in states]
        rules: List[FARule] = sum(rules_list, [])
        more_states = frozenset([rule.follow for rule in rules])

        if more_states.issubset(states):
            return states, rules
        else:
            return self.discover_states_and_rules(more_states.union(states))

    @property
    def to_dfa_design(self):
        start_state = self.nfa_design.to_nfa.current_states
        states, rules = self.discover_states_and_rules(frozenset([start_state]))
        accept_states = [
            state for state in states if self.nfa_design.to_nfa_from(state).accepting
        ]
        return DFADesign(start_state, accept_states, DFARulebook(rules))
