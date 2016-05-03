from __future__ import print_function, unicode_literals

import unittest

from farule import FARule
from utils import detect


class DFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_state(self, state, character):
        return self.rule_for(state, character).follow

    def rule_for(self, state, character):
        return detect(self.rules,
                      lambda rule: rule.applies_to(state, character))


class DFA(object):
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def accepting(self):
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state,
                                                      character)
        return self

    def read_string(self, string):
        for c in string:
            self.read_character(c)
        return self


class DFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_dfa.read_string(string).accepting


class DFATest(unittest.TestCase):
    def test_dfa_rulebook(self):
        rulebook = DFARulebook([
            FARule(1, 'a', 2), FARule(1, 'b', 1), FARule(2, 'a', 2),
            FARule(2, 'b', 3), FARule(3, 'a', 3), FARule(3, 'b', 3)
        ])  #yapf: disable
        self.assertEqual(rulebook.next_state(1, 'a'), 2)
        self.assertEqual(rulebook.next_state(1, 'b'), 1)
        self.assertEqual(rulebook.next_state(2, 'b'), 3)

    def test_dfa(self):
        rulebook = DFARulebook([
            FARule(1, 'a', 2), FARule(1, 'b', 1), FARule(2, 'a', 2),
            FARule(2, 'b', 3), FARule(3, 'a', 3), FARule(3, 'b', 3)
        ])  #yapf: disable

        dfa = DFA(1, [3], rulebook)
        self.assertFalse(dfa.read_character('b').accepting)
        self.assertFalse(any([dfa.read_character('a').accepting for i in range(
            3)]))
        self.assertTrue(dfa.read_character('b').accepting)

        dfa = DFA(1, [3], rulebook)
        self.assertTrue(dfa.read_string('baaab').accepting)

    def test_dfa_design(self):
        rulebook = DFARulebook([
            FARule(1, 'a', 2), FARule(1, 'b', 1), FARule(2, 'a', 2),
            FARule(2, 'b', 3), FARule(3, 'a', 3), FARule(3, 'b', 3)
        ])  #yapf: disable

        dfa_design = DFADesign(1, [3], rulebook)
        self.assertFalse(dfa_design.accepts('a'))
        self.assertFalse(dfa_design.accepts('baa'))
        self.assertTrue(dfa_design.accepts('baba'))


if __name__ == '__main__':
    unittest.main()
