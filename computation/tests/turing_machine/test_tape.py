import unittest

from computation.turing_machine.tape import Tape


class TapeTest(unittest.TestCase):
    def test_tape(self):
        tape = Tape(["1", "0", "1"], "1", [], "_")
        tape = Tape([], "1", [], "_")
        print()
        print(tape)
        print(tape.move_head_left)
        print(tape.move_head_left.write("0"))
        print(tape.move_head_right)
        print(tape.move_head_right.write("0"))
