"""Match repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.match import Match


class IMatchRepository(ABC):
    @abstractmethod
    def find_by_id(self, match_id: str) -> Optional[Match]:
        pass

    @abstractmethod
    def save(self, match: Match) -> Match:
        pass

    @abstractmethod
    def delete(self, match_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Match]:
        pass

    @abstractmethod
    def find_by_tournament(self, tournament_id: str) -> List[Match]:
        pass

    @abstractmethod
    def find_players(self, match_id: str) -> List[dict]:
        pass
