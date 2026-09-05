"""Match repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
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

    @abstractmethod
    def update_court(self, match_id: str, court_id: str) -> None:
        pass

    @abstractmethod
    def finish(self, match_id: str, winner_pair_id: str, winner_team: str) -> None:
        pass

    @abstractmethod
    def find_all_detailed(self) -> List[Dict]:
        pass

    @abstractmethod
    def find_by_id_detailed(self, match_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def update(self, match_id: str, data: Dict) -> None:
        pass
