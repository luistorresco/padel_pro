"""Court repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.court import Court


class ICourtRepository(ABC):
    @abstractmethod
    def find_by_id(self, court_id: str) -> Optional[Court]:
        pass

    @abstractmethod
    def save(self, court: Court) -> Court:
        pass

    @abstractmethod
    def delete(self, court_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Court]:
        pass
