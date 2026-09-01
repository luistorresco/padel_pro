"""Audit logs use cases."""

from domain.exceptions import EntityNotFound


class ListAuditLogsUseCase:
    def __init__(self, audit_log_repo):
        self.audit_log_repo = audit_log_repo

    def execute(self):
        return self.audit_log_repo.list_all(limit=100)


class CreateAuditLogUseCase:
    def __init__(self, audit_log_repo):
        self.audit_log_repo = audit_log_repo

    def execute(self, log_data):
        import uuid
        from domain.entities.audit_log import AuditLog
        log_id = log_data.get("id") or f"audit_{uuid.uuid4().hex[:8]}"
        log = AuditLog(
            log_id=log_id,
            action=log_data["action"],
            target_type=log_data.get("target_type", "unknown"),
            target_id=log_data.get("target_id", ""),
            business_id=log_data.get("business_id"),
            user_id=log_data.get("user_id"),
            details=log_data.get("details"),
            timestamp=log_data.get("timestamp"),
        )
        saved = self.audit_log_repo.save(log)
        return {"id": log_id}
