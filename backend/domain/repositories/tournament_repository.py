"""Tournament repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from domain.entities.tournament import Tournament


class ITournamentRepository(ABC):
    @abstractmethod
    def find_by_id(self, tournament_id: str) -> Optional[Tournament]:
        pass

    @abstractmethod
    def save(self, tournament: Tournament) -> Tournament:
        pass

    @abstractmethod
    def delete(self, tournament_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Tournament]:
        pass

    @abstractmethod
    def find_full(self, tournament_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def register_pair(self, tournament_id: str, pair_id: str, status: str = "REGISTERED") -> None:
        pass

    @abstractmethod
    def register_player(self, tournament_id: str, user_id: str, status: str = "REGISTERED") -> None:
        pass
