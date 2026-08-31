"""Match event repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.match_event import MatchEvent


class IMatchEventRepository(ABC):
    @abstractmethod
    def find_by_match(self, match_id: str) -> List[MatchEvent]:
        pass

    @abstractmethod
    def save(self, event: MatchEvent) -> MatchEvent:
        pass
