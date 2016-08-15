import unittest

from computation.automata.farule import FARule
from computation.automata.dfa import DFARulebook, DFA, DFADesign


class DFATest(unittest.TestCase):
    def test_dfa_rulebook(self):
        rulebook = DFARulebook([
            FARule(1, 'a', 2), FARule(1, 'b', 1), FARule(2, 'a', 2),
            FARule(2, 'b', 3), FARule(3, 'a', 3), FARule(3, 'b', 3)
        ])  # yapf: disable
        self.assertEqual(rulebook.next_state(1, 'a'), 2)
        self.assertEqual(rulebook.next_state(1, 'b'), 1)
        self.assertEqual(rulebook.next_state(2, 'b'), 3)

    def test_dfa(self):
        rulebook = DFARulebook([
            FARule(1, 'a', 2), FARule(1, 'b', 1), FARule(2, 'a', 2),
            FARule(2, 'b', 3), FARule(3, 'a', 3), FARule(3, 'b', 3)
        ])  # yapf: disable

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
        ])  # yapf: disable

        dfa_design = DFADesign(1, [3], rulebook)
        self.assertFalse(dfa_design.accepts('a'))
        self.assertFalse(dfa_design.accepts('baa'))
        self.assertTrue(dfa_design.accepts('baba'))


if __name__ == '__main__':
    unittest.main()
