"""Notifications router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional

from presentation.deps_module import (
    list_notifications_uc,
    create_notification_uc,
    get_current_user,
)

notifications_router = APIRouter()


@notifications_router.get("")
def get_notifications(authorization: Optional[str] = None):
    if not authorization:
        return []
    token = authorization.replace("Bearer ", "")
    from domain.services.auth_service import AuthService
    auth_service = AuthService(secret_key="padel-pro-secret-key-change-in-production")
    payload = auth_service.decode_token(token)
    if not payload:
        return []
    user_id = payload.get("sub")
    if not user_id:
        return []
    try:
        return list_notifications_uc.execute(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@notifications_router.post("")
def create_notification(notification: dict, payload: dict = Depends(get_current_user)):
    try:
        return create_notification_uc.execute(notification)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
