from computation.automata.nfa import FARule, NFA, NFARulebook, NFADesign, NFASimulation


def test_nfa_rulebook():
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
    )
    assert rulebook.next_states([1], "b") == set([1, 2])
    assert rulebook.next_states([1, 2], "a") == set([1, 3])
    assert rulebook.next_states([1, 3], "b") == set([1, 2, 4])


def test_nfa():
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
    assert not (NFA([1], [4], rulebook).accepting)
    assert NFA([1, 2, 4], [4], rulebook).accepting

    nfa = NFA([1], [4], rulebook)
    assert not (nfa.accepting)
    assert not (nfa.read_character("b").accepting)
    assert not (nfa.read_character("a").accepting)
    assert nfa.read_character("b").accepting

    nfa = NFA([1], [4], rulebook)
    assert nfa.read_string("bbbbb").accepting


def test_nfa_design():
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
    )
    nfa = NFADesign(1, [4], rulebook)

    assert nfa.accepts("bab")
    assert nfa.accepts("bbbbb")
    assert not (nfa.accepts("bbabb"))

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
    assert rulebook.alphabet == set(["a", "b"])

    nfa_design = NFADesign(1, [3], rulebook)
    assert nfa_design.to_nfa.current_states == set([1, 2])
    assert nfa_design.to_nfa_from([3]).current_states == set([2, 3])

    nfa = nfa_design.to_nfa_from([2, 3])
    nfa.read_character("b")
    assert nfa.current_states == set([1, 2, 3])

    simulation = NFASimulation(nfa_design)
    assert simulation.next_state([1, 2], "a") == set([1, 2])
    assert simulation.next_state([1, 2], "b") == set([3, 2])
    assert simulation.next_state([3, 2], "b") == set([1, 3, 2])
    assert simulation.next_state([1, 3, 2], "b") == set([1, 3, 2])
    assert simulation.next_state([1, 3, 2], "a") == set([1, 2])

    dfa_design = simulation.to_dfa_design
    assert not (dfa_design.accepts("aaa"))
    assert dfa_design.accepts("aab")
    assert dfa_design.accepts("bbbabb")


def test_free_move():
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
    assert rulebook.next_states([1], None) == set([2, 4])
    assert rulebook.follow_free_moves([1]) == set([1, 2, 4])

    nfa_design = NFADesign(1, [2, 4], rulebook)
    assert nfa_design.accepts("aaaaaa")
    assert nfa_design.accepts("aaa")
    assert nfa_design.accepts("aa")
    assert not (nfa_design.accepts("aaaaa"))
    assert not (nfa_design.accepts("a"))
