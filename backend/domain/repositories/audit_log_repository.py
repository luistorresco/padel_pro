"""Audit log repository port."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.audit_log import AuditLog


class IAuditLogRepository(ABC):
    @abstractmethod
    def save(self, log: AuditLog) -> AuditLog:
        pass

    @abstractmethod
    def list_all(self, limit: int = 100) -> List[AuditLog]:
        pass
