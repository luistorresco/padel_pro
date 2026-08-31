"""Audit log entity."""


class AuditLog:
    def __init__(
        self,
        log_id: str,
        action: str,
        target_type: str,
        target_id: str,
        business_id: str | None = None,
        user_id: str | None = None,
        details: dict | None = None,
        timestamp: str | None = None,
    ):
        self.id = log_id
        self.action = action
        self.target_type = target_type
        self.target_id = target_id
        self.business_id = business_id
        self.user_id = user_id
        self.details = details
        self.timestamp = timestamp
