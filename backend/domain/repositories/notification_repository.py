"""Notification repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.notification import Notification


class INotificationRepository(ABC):
    @abstractmethod
    def find_by_user(self, user_id: str) -> List[Notification]:
        pass

    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: str) -> None:
        pass
