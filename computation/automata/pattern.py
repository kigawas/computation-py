

from .farule import FARule
from .nfa import NFARulebook, NFADesign
from .state import State


class Pattern(object):
    def braket(self, outer_precedence):
        if self.precedence < outer_precedence:
            return '(' + str(self) + ')'
        else:
            return str(self)

    def __repr__(self):
        return '/{}/'.format(self)

    def matches(self, string):
        return self.to_nfa_design.accepts(string)


class Empty(Pattern):
    def __str__(self):
        return ''

    @property
    def precedence(self):
        return 3

    @property
    def to_nfa_design(self):
        start_state = State()
        accept_states = [start_state]
        rulebook = NFARulebook([])
        return NFADesign(start_state, accept_states, rulebook)


class Literal(Pattern):
    def __init__(self, character):
        self.character = character

    def __str__(self):
        return self.character

    @property
    def precedence(self):
        return 3

    @property
    def to_nfa_design(self):
        start_state = State()
        accept_state = State()
        rule = FARule(start_state, self.character, accept_state)
        rulebook = NFARulebook([rule])
        return NFADesign(start_state, [accept_state], rulebook)


class Concatenate(Pattern):
    def __init__(self, first, second):
        self.first, self.second = first, second

    def __str__(self):
        return ''.join([p.braket(self.precedence)
                        for p in [self.first, self.second]])

    @property
    def precedence(self):
        return 1

    @property
    def to_nfa_design(self):
        first_nfa_design, second_nfa_design = (self.first.to_nfa_design,
                                               self.second.to_nfa_design)
        start_state, accept_states = (first_nfa_design.start_state,
                                      second_nfa_design.accept_states)

        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules  # NOQA

        extra_rules = [FARule(state, None, second_nfa_design.start_state)
                       for state in first_nfa_design.accept_states]
        rulebook = NFARulebook(rules + extra_rules)
        return NFADesign(start_state, accept_states, rulebook)


class Choose(Pattern):
    def __init__(self, first, second):
        self.first, self.second = first, second

    def __str__(self):
        return '|'.join([p.braket(self.precedence)
                         for p in [self.first, self.second]])

    @property
    def precedence(self):
        return 0

    @property
    def to_nfa_design(self):
        first_nfa_design, second_nfa_design = (self.first.to_nfa_design,
                                               self.second.to_nfa_design)
        start_state = State()
        accept_states = first_nfa_design.accept_states + second_nfa_design.accept_states  # NOQA

        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules  # NOQA
        extra_rules = [FARule(start_state, None, nfa_design.start_state)
                       for nfa_design in [first_nfa_design, second_nfa_design]]
        rulebook = NFARulebook(rules + extra_rules)
        return NFADesign(start_state, accept_states, rulebook)


class Repeat(Pattern):
    def __init__(self, pattern):
        self.pattern = pattern

    def __str__(self):
        return self.pattern.braket(self.precedence) + '*'

    @property
    def precedence(self):
        return 2

    @property
    def to_nfa_design(self):
        pattern_nfa_design = self.pattern.to_nfa_design
        start_state = State()
        accept_states = pattern_nfa_design.accept_states + [start_state]
        rules = pattern_nfa_design.rulebook.rules
        extra_rules = [
            FARule(accept_state, None, pattern_nfa_design.start_state)
            for accept_state in pattern_nfa_design.accept_states
        ] + [FARule(start_state, None, pattern_nfa_design.start_state)]
        rulebook = NFARulebook(rules + extra_rules)
        return NFADesign(start_state, accept_states, rulebook)
