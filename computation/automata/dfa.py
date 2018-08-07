from computation.automata.utils import detect


class DFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_state(self, state, character):
        return self.rule_for(state, character).follow

    def rule_for(self, state, character):
        return detect(self.rules, lambda rule: rule.applies_to(state, character))


class DFA(object):
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def accepting(self):
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)
        return self

    def read_string(self, string):
        for c in string:
            self.read_character(c)
        return self


class DFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_dfa.read_string(string).accepting
