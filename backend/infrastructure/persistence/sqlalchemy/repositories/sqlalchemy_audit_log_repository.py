"""SQLAlchemy audit log repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.audit_log import AuditLog
from domain.repositories.audit_log_repository import IAuditLogRepository


class SQLAlchemyAuditLogRepository(IAuditLogRepository):
    def __init__(self, engine):
        self.engine = engine

    def save(self, log: AuditLog) -> AuditLog:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO audit_logs (id, business_id, user_id, action, target_type, target_id, details, timestamp)
                VALUES (:id, :business_id, :user_id, :action, :target_type, :target_id, :details, :timestamp)
                ON DUPLICATE KEY UPDATE
                    action = VALUES(action), details = VALUES(details)
            """), {
                "id": log.id, "business_id": log.business_id,
                "user_id": log.user_id, "action": log.action,
                "target_type": log.target_type, "target_id": log.target_id,
                "details": str(log.details) if log.details else None,
                "timestamp": log.timestamp,
            })
        return log

    def list_all(self, limit: int = 100) -> List[AuditLog]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT :limit
            """), {"limit": limit}).mappings().all()
            return [self._to_entity(dict(row)) for row in rows]

    def _to_entity(self, row: dict) -> AuditLog:
        import json
        details = row.get("details")
        if isinstance(details, str):
            try:
                details = json.loads(details)
            except Exception:
                details = None
        return AuditLog(
            log_id=row["id"],
            action=row["action"],
            target_type=row["target_type"],
            target_id=row["target_id"],
            business_id=row.get("business_id"),
            user_id=row.get("user_id"),
            details=details,
            timestamp=row.get("timestamp"),
        )
