from dataclasses import dataclass
from typing import Iterable, List, Optional

from ..utils import detect
from .farule import State
from .state import State as _State


@dataclass(frozen=True)
class Stack:
    contents: List[State]

    def push(self, character):
        return Stack(self.contents + [character])

    @property
    def pop(self):
        return Stack(self.contents[:-1])

    @property
    def top(self):
        return self.contents[-1]

    def __hash__(self):
        return hash(tuple(self.contents))


@dataclass(eq=True)
class PDAConfiguration:
    state: State
    stack: Stack

    STUCK_STATE = _State()

    def __hash__(self):
        return hash(self.state) ^ hash("".join(self.stack.contents))

    @property
    def stuck(self):
        return PDAConfiguration(PDAConfiguration.STUCK_STATE, self.stack)

    @property
    def is_stuck(self):
        return self.state == PDAConfiguration.STUCK_STATE


@dataclass
class PDARule:
    state: State
    character: Optional[str]
    next_state: State
    pop_character: str
    push_characters: Iterable[str]

    def applies_to(self, configuration, character):
        return (
            self.state == configuration.state
            and self.pop_character == configuration.stack.top
            and self.character == character
        )

    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop
        for c in reversed(self.push_characters):
            popped_stack = popped_stack.push(c)
        return popped_stack

    def follow(self, configuration):
        return PDAConfiguration(self.next_state, self.next_stack(configuration))


@dataclass
class DPDARulebook:
    rules: List[PDARule]

    def rule_for(self, configuration, character):
        return detect(
            self.rules, lambda rule: rule.applies_to(configuration, character)
        )

    def next_configuration(self, configuration, character):
        return self.rule_for(configuration, character).follow(configuration)

    def applies_to(self, configuration, character):
        return self.rule_for(configuration, character) is not None

    def follow_free_moves(self, configuration):
        if self.applies_to(configuration, None):
            return self.follow_free_moves(self.next_configuration(configuration, None))
        else:
            return configuration


@dataclass
class DPDA:
    _current_configuration: PDAConfiguration
    accept_states: List[State]
    rulebook: DPDARulebook

    @property
    def accepting(self):
        return self.current_configuration.state in self.accept_states

    def read_character(self, character):
        self._current_configuration = self.next_configuration(character)
        return self

    def read_string(self, string):
        for c in string:
            if not self.is_stuck:
                self.read_character(c)
        return self

    def next_configuration(self, character):
        if self.rulebook.applies_to(self.current_configuration, character):
            return self.rulebook.next_configuration(
                self.current_configuration, character
            )
        else:
            return self.current_configuration.stuck

    @property
    def is_stuck(self):
        return self.current_configuration.is_stuck

    @property
    def current_configuration(self):
        return self.rulebook.follow_free_moves(self._current_configuration)


@dataclass
class DPDADesign:
    start_state: State
    bottom_character: str
    accept_states: List[State]
    rulebook: DPDARulebook

    @property
    def to_dpda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return DPDA(start_configuration, self.accept_states, self.rulebook)

    def accepts(self, string):
        return self.to_dpda.read_string(string).accepting


@dataclass
class NPDARulebook:
    rules: List[PDARule]

    def rule_for(self, configuration, character):
        return [
            rule for rule in self.rules if rule.applies_to(configuration, character)
        ]

    def follow_rules_for(self, configuration, character):
        return [
            rule.follow(configuration)
            for rule in self.rule_for(configuration, character)
        ]

    def next_configurations(self, configurations, character):
        return set(
            sum(
                [self.follow_rules_for(config, character) for config in configurations],
                [],
            )
        )

    def follow_free_moves(self, configurations):
        more_configurations = self.next_configurations(configurations, None)
        if more_configurations.issubset(configurations):
            return configurations
        else:
            return self.follow_free_moves(more_configurations.union(configurations))


@dataclass
class NPDA:
    _current_configurations: PDAConfiguration
    accept_states: Iterable[State]
    rulebook: NPDARulebook

    @property
    def accepting(self):
        return any(
            [
                config.state in self.accept_states
                for config in self.current_configurations
            ]
        )

    def read_character(self, character):
        self._current_configurations = self.rulebook.next_configurations(
            self.current_configurations, character
        )
        return self

    def read_string(self, string):
        for c in string:
            self.read_character(c)
        return self

    @property
    def current_configurations(self):
        return self.rulebook.follow_free_moves(self._current_configurations)


@dataclass
class NPDADesign:
    start_state: State
    bottom_character: str
    accept_states: List[State]
    rulebook: NPDARulebook

    @property
    def to_npda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return NPDA(
            [start_configuration],
            self.accept_states,
            self.rulebook,
        )

    def accepts(self, string):
        return self.to_npda.read_string(string).accepting
