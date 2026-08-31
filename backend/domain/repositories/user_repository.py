"""User repository port (interface)."""

from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        pass
