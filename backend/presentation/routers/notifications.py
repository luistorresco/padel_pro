"""Notifications router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from sqlalchemy import text

from infrastructure.database import engine
from presentation.deps_module import get_current_user

notifications_router = APIRouter()


@notifications_router.get("")
def get_notifications(authorization: Optional[str] = None):
    if not authorization:
        return []
    token = authorization.replace("Bearer ", "")
    from jose import jwt
    from domain.services.auth_service import AuthService
    auth_service = AuthService(secret_key="padel-pro-secret-key-change-in-production")
    payload = auth_service.decode_token(token)
    if not payload:
        return []
    user_id = payload.get("sub")
    if not user_id:
        return []

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM notifications WHERE user_id = :uid ORDER BY timestamp DESC
        """), {"uid": user_id})
        return [dict(row) for row in result.mappings()]


@notifications_router.post("")
def create_notification(notification: dict, payload: dict = Depends(get_current_user)):
    import uuid
    notif_id = notification.get("id") or f"notif_{uuid.uuid4().hex[:8]}"
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO notifications (id, user_id, title, body, timestamp, read_status, type, link_id)
            VALUES (:id, :user_id, :title, :body, :timestamp, :read_status, :type, :link_id)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title), body = VALUES(body), read_status = VALUES(read_status),
                type = VALUES(type), link_id = VALUES(link_id)
        """), {
            "id": notif_id,
            "user_id": notification.get("user_id"),
            "title": notification["title"],
            "body": notification.get("body"),
            "timestamp": notification.get("timestamp"),
            "read_status": 1 if notification.get("read") else 0,
            "type": notification.get("type"),
            "link_id": notification.get("link_id"),
        })
    return {"id": notif_id}
