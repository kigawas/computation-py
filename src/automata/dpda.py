from __future__ import print_function, unicode_literals

import unittest

from farule import FARule
from utils import detect
from state import State


class Stack(object):
    def __init__(self, contents):
        self.contents = contents

    def push(self, character):
        return Stack(self.contents + [character])

    @property
    def pop(self):
        return Stack(self.contents[:-1])

    @property
    def top(self):
        return self.contents[-1]

    def __str__(self):
        return 'Stack({})'.format(self.contents)

    def __eq__(self, other):
        return self.contents == other.contents

    def __ne__(self, other):
        return self.contents != other.contents


class PDAConfiguration(object):
    STUCK_STATE = State()

    def __init__(self, state, stack):
        self.state = state
        self.stack = stack

    def __str__(self):
        return 'State: {}, Stack: {}'.format(self.state, self.stack)

    @property
    def stuck(self):
        return PDAConfiguration(PDAConfiguration.STUCK_STATE, self.stack)

    @property
    def is_stuck(self):
        return self.state == PDAConfiguration.STUCK_STATE


class PDARule(object):
    def __init__(self, state, character, next_state, pop_character,
                 push_characters):
        self.state, self.character = state, character
        self.next_state, self.pop_character = next_state, pop_character
        self.push_characters = push_characters

    def applies_to(self, configuration, character):
        return self.state == configuration.state and self.pop_character == configuration.stack.top and self.character == character

    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop
        for c in reversed(self.push_characters):
            popped_stack = popped_stack.push(c)
        return popped_stack

    def follow(self, configuration):
        return PDAConfiguration(self.next_state,
                                self.next_stack(configuration))


class DPDARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def rule_for(self, configuration, character):
        return detect(self.rules,
                      lambda rule: rule.applies_to(configuration, character))

    def next_configuration(self, configuration, character):
        return self.rule_for(configuration, character).follow(configuration)

    def applies_to(self, configuration, character):
        return self.rule_for(configuration, character) is not None

    def follow_free_moves(self, configuration):
        if self.applies_to(configuration, None):
            return self.follow_free_moves(self.next_configuration(
                configuration, None))
        else:
            return configuration


class DPDA(object):
    def __init__(self, current_configuration, accept_states, rulebook):
        self._current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def accepting(self):
        return self.current_configuration.state in self.accept_states

    def read_character(self, character):
        self._current_configuration = self.next_configuration(character)
        return self

    def read_string(self, string):
        for c in string:
            if not self.is_stuck:
                self.read_character(c)
        return self

    def next_configuration(self, character):
        if self.rulebook.applies_to(self.current_configuration, character):
            return self.rulebook.next_configuration(self.current_configuration,
                                                    character)
        else:
            return self.current_configuration.stuck

    @property
    def is_stuck(self):
        return self.current_configuration.is_stuck

    @property
    def current_configuration(self):
        return self.rulebook.follow_free_moves(self._current_configuration)


class DPDADesign(object):
    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self.start_state, self.bottom_character = start_state, bottom_character
        self.accept_states, self.rulebook = accept_states, rulebook

    @property
    def to_dpda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return DPDA(start_configuration, self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_dpda.read_string(string).accepting


class PDATest(unittest.TestCase):
    def test_pda_rule(self):
        rule = PDARule(1, '(', 2, '$', ['b', '$'])
        configuration = PDAConfiguration(1, Stack(['$']))
        self.assertTrue(rule.applies_to(configuration, '('))

    def test_pda_rulebook(self):
        configuration = PDAConfiguration(1, Stack(['$']))
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']), PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])  #yapf: disable

        configuration = rulebook.next_configuration(configuration, '(')
        self.assertEqual(configuration.stack, Stack(['$', 'b']))

    def test_dpda(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']), PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])  #yapf: disable
        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        self.assertTrue(dpda.accepting)
        self.assertFalse(dpda.read_string('(()').accepting)
        self.assertEqual(dpda.current_configuration.state, 2)

        configuration = PDAConfiguration(2, Stack(['$']))

        with self.assertRaises(RuntimeError):
            DPDARulebook([PDARule(1, None, 1, '$', ['$'])]).follow_free_moves(
                PDAConfiguration(1, Stack(['$'])))

        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        self.assertFalse(dpda.read_string('(()(').accepting)
        self.assertTrue(dpda.read_string('))()').accepting)

    def test_dpda_design(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']), PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])  #yapf: disable
        dpda_design = DPDADesign(1, '$', [1], rulebook)
        self.assertTrue(dpda_design.accepts('(((((((((())))))))))'))
        self.assertTrue(dpda_design.accepts('()(())((()))(()(()))'))
        self.assertFalse(dpda_design.accepts('(()(()(()()(()()))()'))
        self.assertFalse(dpda_design.accepts('())'))

        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        dpda.read_string('())')
        self.assertFalse(dpda.accepting)
        self.assertTrue(dpda.is_stuck)


if __name__ == '__main__':
    unittest.main()
