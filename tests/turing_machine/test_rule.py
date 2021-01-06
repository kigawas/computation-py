from computation.turing_machine.rule import (
    DTM,
    Direction,
    DTMRulebook,
    Tape,
    TMConfiguration,
    TMRule,
)

# increment binary number rulebook
rulebook = DTMRulebook(
    [
        TMRule(1, "0", 2, "1", Direction.RIGHT),
        TMRule(1, "1", 1, "0", Direction.LEFT),
        TMRule(1, "_", 2, "1", Direction.RIGHT),
        TMRule(2, "0", 2, "0", Direction.RIGHT),
        TMRule(2, "1", 2, "1", Direction.RIGHT),
        TMRule(2, "_", 3, "_", Direction.LEFT),
    ]
)


def test_rule():
    dtm = DTM(
        TMConfiguration(1, Tape(["1", "0", "1"], "1", ["_"])),
        [3],
        rulebook,
    )
    dtm.run()
    assert dtm.current_configuration.state == 3
    assert dtm.current_configuration.tape == Tape(["1", "1", "0"], "0", ["_"])

    dtm = DTM(
        TMConfiguration(1, Tape(["1", "2", "1"], "1", ["_"])),
        [3],
        rulebook,
    )
    dtm.run()
    assert dtm.is_stuck
