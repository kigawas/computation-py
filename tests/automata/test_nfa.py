import unittest

from computation.automata.nfa import FARule, NFA, NFARulebook, NFADesign, NFASimulation


class NFATest(unittest.TestCase):
    def test_nfa_rulebook(self):
        rulebook = NFARulebook(
            [
                FARule(1, "a", 1),
                FARule(1, "b", 1),
                FARule(1, "b", 2),
                FARule(2, "a", 3),
                FARule(2, "b", 3),
                FARule(3, "a", 4),
                FARule(3, "b", 4),
            ]
        )  # yapf: disable
        self.assertEqual(rulebook.next_states([1], "b"), set([1, 2]))
        self.assertEqual(rulebook.next_states([1, 2], "a"), set([1, 3]))
        self.assertEqual(rulebook.next_states([1, 3], "b"), set([1, 2, 4]))

    def test_nfa(self):
        rulebook = NFARulebook(
            [
                FARule(1, "a", 1),
                FARule(1, "b", 1),
                FARule(1, "b", 2),
                FARule(2, "a", 3),
                FARule(2, "b", 3),
                FARule(3, "a", 4),
                FARule(3, "b", 4),
            ]
        )  # yapf: disable
        self.assertFalse(NFA([1], [4], rulebook).accepting)
        self.assertTrue(NFA([1, 2, 4], [4], rulebook).accepting)

        nfa = NFA([1], [4], rulebook)
        self.assertFalse(nfa.accepting)
        self.assertFalse(nfa.read_character("b").accepting)
        self.assertFalse(nfa.read_character("a").accepting)
        self.assertTrue(nfa.read_character("b").accepting)

        nfa = NFA([1], [4], rulebook)
        self.assertTrue(nfa.read_string("bbbbb").accepting)

    def test_nfa_design(self):
        rulebook = NFARulebook(
            [
                FARule(1, "a", 1),
                FARule(1, "b", 1),
                FARule(1, "b", 2),
                FARule(2, "a", 3),
                FARule(2, "b", 3),
                FARule(3, "a", 4),
                FARule(3, "b", 4),
            ]
        )  # yapf: disable
        nfa = NFADesign(1, [4], rulebook)

        self.assertTrue(nfa.accepts("bab"))
        self.assertTrue(nfa.accepts("bbbbb"))
        self.assertFalse(nfa.accepts("bbabb"))

        rulebook = NFARulebook(
            [
                FARule(1, "a", 1),
                FARule(1, "a", 2),
                FARule(1, None, 2),
                FARule(2, "b", 3),
                FARule(3, "b", 1),
                FARule(3, None, 2),
            ]
        )  # yapf: disable
        self.assertEqual(rulebook.alphabet, set(["a", "b"]))

        nfa_design = NFADesign(1, [3], rulebook)
        self.assertEqual(nfa_design.to_nfa.current_states, set([1, 2]))
        self.assertEqual(nfa_design.to_nfa_from([3]).current_states, set([2, 3]))

        nfa = nfa_design.to_nfa_from([2, 3])
        nfa.read_character("b")
        self.assertEqual(nfa.current_states, set([1, 2, 3]))

        simulation = NFASimulation(nfa_design)
        self.assertEqual(simulation.next_state([1, 2], "a"), set([1, 2]))
        self.assertEqual(simulation.next_state([1, 2], "b"), set([3, 2]))
        self.assertEqual(simulation.next_state([3, 2], "b"), set([1, 3, 2]))
        self.assertEqual(simulation.next_state([1, 3, 2], "b"), set([1, 3, 2]))
        self.assertEqual(simulation.next_state([1, 3, 2], "a"), set([1, 2]))

        dfa_design = simulation.to_dfa_design
        self.assertFalse(dfa_design.accepts("aaa"))
        self.assertTrue(dfa_design.accepts("aab"))
        self.assertTrue(dfa_design.accepts("bbbabb"))

    def test_free_move(self):
        rulebook = NFARulebook(
            [
                FARule(1, None, 2),
                FARule(1, None, 4),
                FARule(2, "a", 3),
                FARule(3, "a", 2),
                FARule(4, "a", 5),
                FARule(5, "a", 6),
                FARule(6, "a", 4),
            ]
        )  # yapf: disable
        self.assertEqual(rulebook.next_states([1], None), set([2, 4]))
        self.assertEqual(rulebook.follow_free_moves([1]), set([1, 2, 4]))

        nfa_design = NFADesign(1, [2, 4], rulebook)
        self.assertTrue(nfa_design.accepts("aaaaaa"))
        self.assertTrue(nfa_design.accepts("aaa"))
        self.assertTrue(nfa_design.accepts("aa"))
        self.assertFalse(nfa_design.accepts("aaaaa"))
        self.assertFalse(nfa_design.accepts("a"))


if __name__ == "__main__":
    unittest.main()
