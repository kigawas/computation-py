from computation.automata.farule import FARule
from computation.automata.dfa import DFARulebook, DFA, DFADesign


def test_dfa_rulebook():
    rulebook = DFARulebook(
        [
            FARule(1, "a", 2),
            FARule(1, "b", 1),
            FARule(2, "a", 2),
            FARule(2, "b", 3),
            FARule(3, "a", 3),
            FARule(3, "b", 3),
        ]
    )
    assert rulebook.next_state(1, "a") == 2
    assert rulebook.next_state(1, "b") == 1
    assert rulebook.next_state(2, "b") == 3


def test_dfa():
    rulebook = DFARulebook(
        [
            FARule(1, "a", 2),
            FARule(1, "b", 1),
            FARule(2, "a", 2),
            FARule(2, "b", 3),
            FARule(3, "a", 3),
            FARule(3, "b", 3),
        ]
    )
    dfa = DFA(1, [3], rulebook)
    assert not (dfa.read_character("b").accepting)
    assert not (any([dfa.read_character("a").accepting for i in range(3)]))
    assert dfa.read_character("b").accepting

    dfa = DFA(1, [3], rulebook)
    assert dfa.read_string("baaab").accepting


def test_dfa_design():
    rulebook = DFARulebook(
        [
            FARule(1, "a", 2),
            FARule(1, "b", 1),
            FARule(2, "a", 2),
            FARule(2, "b", 3),
            FARule(3, "a", 3),
            FARule(3, "b", 3),
        ]
    )

    dfa_design = DFADesign(1, [3], rulebook)
    assert not (dfa_design.accepts("a"))
    assert not (dfa_design.accepts("baa"))
    assert dfa_design.accepts("baba")
