"""User points repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.user_points import UserPoints


class IUserPointsRepository(ABC):
    @abstractmethod
    def find_by_user(self, user_id: str) -> List[UserPoints]:
        pass

    @abstractmethod
    def save(self, user_points: UserPoints) -> UserPoints:
        pass
