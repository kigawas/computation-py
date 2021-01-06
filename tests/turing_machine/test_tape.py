from computation.turing_machine.tape import Tape, TMConfiguration
from computation.turing_machine.rule import TMRule


def test_tape():
    tape = Tape(["1", "0", "1"], "1", [])
    assert tape.move_head_left == Tape(["1", "0"], "1", ["1"])
    assert tape.move_head_left.write("0") == Tape(["1", "0"], "0", ["1"])
    assert tape.move_head_right == Tape(["1", "0", "1", "1"], "_", [])
    assert tape.move_head_right.write("0") == Tape(["1", "0", "1", "1"], "0", [])

    rule = TMRule(1, "0", 2, "1", "right")
    config = TMConfiguration(1, Tape([], "0", []))
    assert rule.follow(config) == TMConfiguration(2, Tape(["1"], "_", []))
