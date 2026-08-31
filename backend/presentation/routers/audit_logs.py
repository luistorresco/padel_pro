"""Audit logs router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from sqlalchemy import text

from infrastructure.database import engine
from presentation.deps_module import require_admin

audit_logs_router = APIRouter()


@audit_logs_router.get("")
def get_audit_logs(payload: dict = Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 100
        """))
        return [dict(row) for row in result.mappings()]


@audit_logs_router.post("")
def create_audit_log(log: dict, payload: dict = Depends(require_admin)):
    import uuid
    log_id = log.get("id") or f"audit_{uuid.uuid4().hex[:8]}"
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO audit_logs (id, business_id, user_id, action, target_type, target_id, details, timestamp)
            VALUES (:id, :business_id, :user_id, :action, :target_type, :target_id, :details, :timestamp)
            ON DUPLICATE KEY UPDATE
                action = VALUES(action), details = VALUES(details)
        """), {
            "id": log_id,
            "business_id": log.get("business_id"),
            "user_id": log.get("user_id"),
            "action": log.get("action"),
            "target_type": log.get("target_type", "unknown"),
            "target_id": log.get("target_id", ""),
            "details": str(log.get("details")) if log.get("details") else None,
            "timestamp": log.get("timestamp"),
        })
    return {"id": log_id}
