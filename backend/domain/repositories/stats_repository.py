from abc import ABC, abstractmethod
from typing import Dict, Any


class StatsRepository(ABC):
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_db_users(self) -> list:
        ...

    @abstractmethod
    def get_db_matches(self) -> list:
        ...
