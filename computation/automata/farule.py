from __future__ import annotations

from dataclasses import dataclass
from typing import List, FrozenSet, Iterable, Optional, Union

from .utils import detect


@dataclass(frozen=True)
class FARule:
    state: Union[int, FrozenSet[int]]
    character: Optional[str]
    next_state: Union[int, FrozenSet[int]]

    @property
    def follow(self) -> Union[int, FrozenSet[int]]:
        return self.next_state

    def applies_to(self, state: int, character: Optional[str]) -> bool:
        if character is None:
            return self.state == state and self.character is None
        return self.state == state and self.character == character

    def reverse(self) -> FARule:
        return FARule(self.next_state, self.character, self.state)


@dataclass(frozen=True)
class DFARulebook:
    rules: List[FARule]

    def rule_for(self, state: int, character: Optional[str]) -> FARule:
        return detect(self.rules, lambda rule: rule.applies_to(state, character))

    def next_state(self, state: int, character: Optional[str]) -> int:
        return self.rule_for(state, character).follow


@dataclass(frozen=True)
class NFARulebook:
    rules: List[FARule]

    @property
    def alphabet(self) -> FrozenSet[str]:
        return frozenset(
            [rule.character for rule in self.rules if rule.character is not None]
        )

    def rules_for(self, state: int, character: Optional[str]) -> List[FARule]:
        return [r for r in self.rules if r.applies_to(state, character)]

    def follow_rules_for(self, state: int, character: Optional[str]) -> List[int]:
        return [r.follow for r in self.rules_for(state, character)]

    def next_states(
        self, states: Iterable[int], character: Optional[str]
    ) -> FrozenSet[int]:
        next_states = [self.follow_rules_for(s, character) for s in states]
        return frozenset(sum(next_states, []))

    def follow_free_moves(self, states: Iterable[int]) -> Iterable[int]:
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(more_states.union(states))
