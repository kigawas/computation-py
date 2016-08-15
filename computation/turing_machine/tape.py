

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
