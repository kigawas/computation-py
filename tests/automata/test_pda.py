import pytest

from computation.automata.pda import (
    Stack,
    PDAConfiguration,
    PDARule,
    DPDARulebook,
    DPDA,
    DPDADesign,
    NPDARulebook,
    NPDA,
    NPDADesign,
)


def test_pda_rule():
    rule = PDARule(1, "(", 2, "$", ["b", "$"])
    configuration = PDAConfiguration(1, Stack(["$"]))
    assert rule.applies_to(configuration, "(")


def test_pda_config():
    config1 = PDAConfiguration(3, Stack(["$"]))
    config2 = PDAConfiguration(3, Stack(["$"]))
    assert config1 == config2
    assert set([config1, config2]) == set([config1])


def test_pda_rulebook():
    configuration = PDAConfiguration(1, Stack(["$"]))
    rulebook = DPDARulebook(
        [
            PDARule(1, "(", 2, "$", ["b", "$"]),
            PDARule(2, "(", 2, "b", ["b", "b"]),
            PDARule(2, ")", 2, "b", []),
            PDARule(2, None, 1, "$", ["$"]),
        ]
    )

    configuration = rulebook.next_configuration(configuration, "(")
    assert configuration.stack == Stack(["$", "b"])


def test_dpda():
    rulebook = DPDARulebook(
        [
            PDARule(1, "(", 2, "$", ["b", "$"]),
            PDARule(2, "(", 2, "b", ["b", "b"]),
            PDARule(2, ")", 2, "b", []),
            PDARule(2, None, 1, "$", ["$"]),
        ]
    )
    dpda = DPDA(PDAConfiguration(1, Stack(["$"])), [1], rulebook)
    assert dpda.accepting
    assert not (dpda.read_string("(()").accepting)
    assert dpda.current_configuration.state == 2

    with pytest.raises(RuntimeError):
        DPDARulebook([PDARule(1, None, 1, "$", ["$"])]).follow_free_moves(
            PDAConfiguration(1, Stack(["$"]))
        )

    dpda = DPDA(PDAConfiguration(1, Stack(["$"])), [1], rulebook)
    assert not (dpda.read_string("(()(").accepting)
    assert dpda.read_string("))()").accepting


def test_dpda_design():
    rulebook = DPDARulebook(
        [
            PDARule(1, "(", 2, "$", ["b", "$"]),
            PDARule(2, "(", 2, "b", ["b", "b"]),
            PDARule(2, ")", 2, "b", []),
            PDARule(2, None, 1, "$", ["$"]),
        ]
    )
    dpda_design = DPDADesign(1, "$", [1], rulebook)
    assert dpda_design.accepts("(((((((((())))))))))")
    assert dpda_design.accepts("()(())((()))(()(()))")
    assert not (dpda_design.accepts("(()(()(()()(()()))()"))
    assert not (dpda_design.accepts("())"))

    dpda = DPDA(PDAConfiguration(1, Stack(["$"])), [1], rulebook)
    dpda.read_string("())")
    assert not (dpda.accepting)
    assert dpda.is_stuck


def test_npda_design():
    rulebook = NPDARulebook(
        [
            PDARule(1, "a", 1, "$", ["a", "$"]),
            PDARule(1, "a", 1, "a", ["a", "a"]),
            PDARule(1, "a", 1, "b", ["a", "b"]),
            PDARule(1, "b", 1, "$", ["b", "$"]),
            PDARule(1, "b", 1, "a", ["b", "a"]),
            PDARule(1, "b", 1, "b", ["b", "b"]),
            PDARule(1, None, 2, "$", ["$"]),
            PDARule(1, None, 2, "a", ["a"]),
            PDARule(1, None, 2, "b", ["b"]),
            PDARule(2, "a", 2, "a", []),
            PDARule(2, "b", 2, "b", []),
            PDARule(2, None, 3, "$", ["$"]),
        ]
    )
    configuration = PDAConfiguration(1, Stack(["$"]))
    npda = NPDA([configuration], [3], rulebook)
    assert npda.accepting
    assert not (npda.read_string("abb").accepting)
    assert PDAConfiguration(
        1, Stack(["$", "a", "b", "b"]) in npda.current_configurations
    )
    assert npda.read_character("a").accepting
    assert PDAConfiguration(
        1, Stack(["$", "a", "b", "b", "a"]) in npda.current_configurations
    )
    npda_design = NPDADesign(1, "$", [3], rulebook)
    assert npda_design.accepts("abba")
    assert npda_design.accepts("babbaabbab")
    assert not (npda_design.accepts("abb"))
