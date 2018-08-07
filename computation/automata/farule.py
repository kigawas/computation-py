class FARule(object):
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def __repr__(self):
        return "FARule({}, {}, {})".format(self.state, self.character, self.next_state)

    def __str__(self):
        return "#<FARule {} --{}--> {}".format(
            self.state, self.character, self.next_state
        )

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    @property
    def follow(self):
        return self.next_state
