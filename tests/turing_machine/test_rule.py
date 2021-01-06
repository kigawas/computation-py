from computation.turing_machine.rule import (
    DTMRulebook,
    TMConfiguration,
    TMRule,
    DTM,
    Tape,
    Direction,
)

# add1 rulebook
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
    tape = Tape(["1", "0", "1"], "1", ["_"])

    configuration = TMConfiguration(1, tape)
    dtm = DTM(
        configuration,
        [3],
        rulebook,
    )
    dtm.run()
    assert dtm.current_configuration.state == 3
    assert dtm.current_configuration.tape == Tape(["1", "1", "0"], "0", ["_"])
