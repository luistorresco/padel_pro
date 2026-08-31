from abc import ABC, abstractmethod
from typing import Dict, Any


class MigrationRepository(ABC):
    @abstractmethod
    def apply_migrations(self) -> Dict[str, str]:
        ...
