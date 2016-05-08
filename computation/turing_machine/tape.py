from __future__ import print_function, unicode_literals

import unittest


class Tape(object):
    def __init__(self, left, middle, right, blank):
        assert isinstance(left, list) and isinstance(right, list)
        self.left, self.middle, self.right, self.blank = (left, middle, right,
                                                          blank)

    def __str__(self):
        return '<Tape: {}({}){}>'.format(''.join(self.left), self.middle,
                                         ''.join(self.right))

    def write(self, character):
        return Tape(self.left, character, self.right, self.blank)

    @property
    def move_head_left(self):
        left = self.left[:-1]
        middle = self.left[-1] if self.left != [] else self.blank
        right = [self.middle] + self.right
        return Tape(left, middle, right, self.blank)

    @property
    def move_head_right(self):
        left = self.left + [self.middle]
        middle = self.right[0] if self.right != [] else self.blank
        right = self.right[1:]
        return Tape(left, middle, right, self.blank)


class TapeTest(unittest.TestCase):
    def test_tape(self):
        tape = Tape(['1', '0', '1'], '1', [], '_')
        tape = Tape([], '1', [], '_')
        print(tape)
        print(tape.move_head_left)
        print(tape.move_head_left.write('0'))
        print(tape.move_head_right)
        print(tape.move_head_right.write('0'))


if __name__ == '__main__':
    unittest.main()
