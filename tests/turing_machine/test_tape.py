from computation.turing_machine.tape import Tape, TMRule, TMConfiguration, DTMRulebook


def test_tape():
    tape = Tape(["1", "0", "1"], "1", [], "_")
    print()
    print(tape)
    print(tape.move_head_left)
    print(tape.move_head_left.write("0"))
    print(tape.move_head_right)
    print(tape.move_head_right.write("0"))

    rule = TMRule(1, "0", 2, "1", "right")
    print(rule.follow(TMConfiguration(1, Tape([], "0", [], "_"))))

    rulebook = DTMRulebook(
        [
            TMRule(1, "0", 2, "1", "right"),
            TMRule(1, "1", 1, "0", "left"),
            TMRule(1, "_", 2, "1", "right"),
            TMRule(2, "0", 2, "0", "right"),
            TMRule(2, "1", 2, "1", "right"),
            TMRule(2, "_", 3, "_", "left"),
        ]
    )
    configuration = TMConfiguration(1, tape)
    print(configuration)
    configuration = rulebook.next_configuration(configuration)
    print(configuration)
    configuration = rulebook.next_configuration(configuration)
    print(configuration)
    configuration = rulebook.next_configuration(configuration)
    print(configuration)
