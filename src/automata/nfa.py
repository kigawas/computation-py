from __future__ import print_function, unicode_literals

import unittest

from farule import FARule


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

    def accepts(self, string):
        return self.to_nfa.read_string(string).accepting


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

    def test_free_move(self):
        rulebook = NFARulebook([
            FARule(1, None, 2), FARule(1, None, 4), FARule(2, 'a', 3),
            FARule(3, 'a', 2), FARule(4, 'a', 5), FARule(5, 'a', 6),
            FARule(6, 'a', 4)
        ])  #yapf: disable
        self.assertEqual(rulebook.next_states([1], None), set([2, 4]))
        self.assertEqual(rulebook.follow_free_moves([1]), set([1, 2, 4]))
        nfa_design = NFADesign(1,[2,4],rulebook)
        self.assertTrue(nfa_design.accepts('aaaaaa'))
        self.assertTrue(nfa_design.accepts('aaa'))
        self.assertTrue(nfa_design.accepts('aa'))
        self.assertFalse(nfa_design.accepts('aaaaa'))
        self.assertFalse(nfa_design.accepts('a'))

if __name__ == '__main__':
    unittest.main()
