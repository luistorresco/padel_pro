"""Pair repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from domain.entities.pair import Pair


class IPairRepository(ABC):
    @abstractmethod
    def find_by_id(self, pair_id: str) -> Optional[Pair]:
        pass

    @abstractmethod
    def save(self, pair: Pair) -> Pair:
        pass

    @abstractmethod
    def delete(self, pair_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Pair]:
        pass

    @abstractmethod
    def find_by_players(self, player1_id: str, player2_id: str) -> Optional[Pair]:
        pass

    @abstractmethod
    def find_with_players(self, pair_id: str) -> Optional[Dict]:
        pass
