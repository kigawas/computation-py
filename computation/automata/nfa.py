from __future__ import print_function, unicode_literals

import unittest

from farule import FARule
from dfa import DFADesign, DFARulebook


class NFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def rules_for(self, state, character):
        return [r for r in self.rules if r.applies_to(state, character)]

    def follow_rules_for(self, state, character):
        return [r.follow for r in self.rules_for(state, character)]

    def next_states(self, states, character):
        return set(sum(
            [self.follow_rules_for(s, character) for s in states], []))

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(more_states.union(states))

    @property
    def alphabet(self):
        return set([rule.character
                    for rule in self.rules if rule.character is not None])


class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self._current_states = set(current_states)
        self.accept_states = set(accept_states)
        self.rulebook = rulebook

    @property
    def accepting(self):
        return not set.isdisjoint(self.current_states, self.accept_states)

    def read_character(self, character):
        self._current_states = self.rulebook.next_states(self.current_states,
                                                         character)
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
        return self.nfa_design.to_nfa_from(set(state)).read_character(
            character).current_states

    def rules_for(self, state):
        return [FARule(
            set(state), character, self.next_state(state, character))
                for character in self.nfa_design.rulebook.alphabet]

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
        accept_states = [state
                         for state in states
                         if self.nfa_design.to_nfa_from(state).accepting]
        return DFADesign(start_state, accept_states, DFARulebook(rules))


class NFATest(unittest.TestCase):
    def test_nfa_rulebook(self):
        rulebook = NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
            FARule(2, 'a', 3), FARule(2, 'b', 3), FARule(3, 'a', 4),
            FARule(3, 'b', 4)
        ])  #yapf: disable
        self.assertEqual(rulebook.next_states([1], 'b'), set([1, 2]))
        self.assertEqual(rulebook.next_states([1, 2], 'a'), set([1, 3]))
        self.assertEqual(rulebook.next_states([1, 3], 'b'), set([1, 2, 4]))

    def test_nfa(self):
        rulebook = NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
            FARule(2, 'a', 3), FARule(2, 'b', 3), FARule(3, 'a', 4),
            FARule(3, 'b', 4)
        ])  #yapf: disable
        self.assertFalse(NFA([1], [4], rulebook).accepting)
        self.assertTrue(NFA([1, 2, 4], [4], rulebook).accepting)

        nfa = NFA([1], [4], rulebook)
        self.assertFalse(nfa.accepting)
        self.assertFalse(nfa.read_character('b').accepting)
        self.assertFalse(nfa.read_character('a').accepting)
        self.assertTrue(nfa.read_character('b').accepting)

        nfa = NFA([1], [4], rulebook)
        self.assertTrue(nfa.read_string('bbbbb').accepting)

    def test_nfa_design(self):
        rulebook = NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
            FARule(2, 'a', 3), FARule(2, 'b', 3), FARule(3, 'a', 4),
            FARule(3, 'b', 4)
        ])  #yapf: disable
        nfa = NFADesign(1, [4], rulebook)

        self.assertTrue(nfa.accepts('bab'))
        self.assertTrue(nfa.accepts('bbbbb'))
        self.assertFalse(nfa.accepts('bbabb'))

        rulebook = NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'a', 2), FARule(1, None, 2),
            FARule(2, 'b', 3), FARule(3, 'b', 1), FARule(3, None, 2)
        ])  #yapf: disable
        self.assertEqual(rulebook.alphabet, set(['a', 'b']))

        nfa_design = NFADesign(1, [3], rulebook)
        self.assertEqual(nfa_design.to_nfa.current_states, set([1, 2]))
        self.assertEqual(
            nfa_design.to_nfa_from([3]).current_states, set([2, 3]))

        nfa = nfa_design.to_nfa_from([2, 3])
        nfa.read_character('b')
        self.assertEqual(nfa.current_states, set([1, 2, 3]))

        simulation = NFASimulation(nfa_design)
        self.assertEqual(simulation.next_state([1, 2], 'a'), set([1, 2]))
        self.assertEqual(simulation.next_state([1, 2], 'b'), set([3, 2]))
        self.assertEqual(simulation.next_state([3, 2], 'b'), set([1, 3, 2]))
        self.assertEqual(simulation.next_state([1, 3, 2], 'b'), set([1, 3, 2]))
        self.assertEqual(simulation.next_state([1, 3, 2], 'a'), set([1, 2]))

        dfa_design = simulation.to_dfa_design
        self.assertFalse(dfa_design.accepts('aaa'))
        self.assertTrue(dfa_design.accepts('aab'))
        self.assertTrue(dfa_design.accepts('bbbabb'))

    def test_free_move(self):
        rulebook = NFARulebook([
            FARule(1, None, 2), FARule(1, None, 4), FARule(2, 'a', 3),
            FARule(3, 'a', 2), FARule(4, 'a', 5), FARule(5, 'a', 6),
            FARule(6, 'a', 4)
        ])  #yapf: disable
        self.assertEqual(rulebook.next_states([1], None), set([2, 4]))
        self.assertEqual(rulebook.follow_free_moves([1]), set([1, 2, 4]))

        nfa_design = NFADesign(1, [2, 4], rulebook)
        self.assertTrue(nfa_design.accepts('aaaaaa'))
        self.assertTrue(nfa_design.accepts('aaa'))
        self.assertTrue(nfa_design.accepts('aa'))
        self.assertFalse(nfa_design.accepts('aaaaa'))
        self.assertFalse(nfa_design.accepts('a'))


if __name__ == '__main__':
    unittest.main()
