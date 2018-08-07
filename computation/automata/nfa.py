

from computation.automata.farule import FARule
from computation.automata.dfa import DFADesign, DFARulebook


class NFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def rules_for(self, state, character):
        return [r for r in self.rules if r.applies_to(state, character)]

    def follow_rules_for(self, state, character):
        return [r.follow for r in self.rules_for(state, character)]

    def next_states(self, states, character):
        return set(sum([self.follow_rules_for(s, character) for s in states], []))

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(more_states.union(states))

    @property
    def alphabet(self):
        return set(
            [rule.character for rule in self.rules if rule.character is not None]
        )


class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self._current_states = set(current_states)
        self.accept_states = set(accept_states)
        self.rulebook = rulebook

    @property
    def accepting(self):
        return not set.isdisjoint(self.current_states, self.accept_states)

    def read_character(self, character):
        self._current_states = self.rulebook.next_states(self.current_states, character)
        return self

    def read_string(self, string):
        for c in string:
            self.read_character(c)
        return self

    @property
    def current_states(self):
        return self.rulebook.follow_free_moves(self._current_states)


class NFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def to_nfa(self):
        return NFA(set([self.start_state]), self.accept_states, self.rulebook)

    def to_nfa_from(self, current_states):
        return NFA(set(current_states), self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_nfa.read_string(string).accepting


class NFASimulation(object):
    def __init__(self, nfa_design):
        self.nfa_design = nfa_design

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
