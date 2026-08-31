"""Role repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.role import Role


class IRoleRepository(ABC):
    @abstractmethod
    def find_by_id(self, role_id: int) -> Optional[Role]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Role]:
        pass

    @abstractmethod
    def list_all(self) -> List[Role]:
        pass

    @abstractmethod
    def save(self, role: Role) -> Role:
        pass
