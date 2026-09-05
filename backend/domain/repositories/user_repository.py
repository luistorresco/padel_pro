"""User repository port (interface)."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
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

    @abstractmethod
    def find_auth_by_email(self, email: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def find_role_by_user(self, user_id: str) -> Optional[str]:
        pass

    @abstractmethod
    def update_last_login(self, user_id: str) -> None:
        pass

    @abstractmethod
    def find_privacy(self, user_id: str) -> Dict:
        pass

    @abstractmethod
    def create_auth(self, user_id: str, email: str, hashed_password: str) -> None:
        pass

    @abstractmethod
    def assign_role(self, user_id: str, role_name: str) -> None:
        pass

    @abstractmethod
    def hard_delete(self, user_id: str) -> None:
        pass

    @abstractmethod
    def find_with_role(self, user_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def list_by_inviter(self, inviter_id: str, limit: int = 100) -> List[User]:
        pass

    @abstractmethod
    def find_guest_by_invitation_code(self, invitation_code: str) -> Optional[User]:
        pass

    @abstractmethod
    def update_privacy(self, user_id: str, privacy_data: Dict) -> None:
        pass
