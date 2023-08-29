from __future__ import annotations

from dataclasses import dataclass
from typing import Any, FrozenSet, Iterable, Optional, Union

from ..exceptions import Unreachable
from ..utils import detect

State = Union[int, Any]


@dataclass(frozen=True)
class FARule:
    state: State
    character: Optional[str]
    next_state: State

    @property
    def follow(self) -> State:
        return self.next_state

    def applies_to(self, state: State, character: Optional[str]) -> bool:
        if character is None:
            return self.state == state and self.character is None

        return self.state == state and self.character == character


@dataclass(frozen=True)
class DFARulebook:
    rules: list[FARule]

    def rule_for(self, state: State, character: Optional[str]) -> Optional[FARule]:
        return detect(self.rules, lambda rule: rule.applies_to(state, character))

    def next_state(self, state: State, character: Optional[str]) -> State:
        rule = self.rule_for(state, character)
        if not rule:
            raise Unreachable
        return rule.follow


@dataclass(frozen=True)
class NFARulebook:
    rules: list[FARule]

    @property
    def alphabet(self) -> FrozenSet[str]:
        return frozenset(
            [rule.character for rule in self.rules if rule.character is not None]
        )

    def rules_for(self, state: State, character: Optional[str]) -> list[FARule]:
        return [r for r in self.rules if r.applies_to(state, character)]

    def follow_rules_for(self, state: State, character: Optional[str]) -> list[State]:
        return [r.follow for r in self.rules_for(state, character)]

    def next_states(
        self, states: Iterable[State], character: Optional[str]
    ) -> FrozenSet[State]:
        next_states = [self.follow_rules_for(s, character) for s in states]
        return frozenset(sum(next_states, []))

    def follow_free_moves(self, states: Iterable[int]) -> Iterable[State]:
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(more_states.union(states))
