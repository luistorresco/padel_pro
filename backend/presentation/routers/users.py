"""Users router."""

import logging
import os
from fastapi import APIRouter, Depends, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional, List

from presentation.deps_module import (
    get_current_user,
    require_admin,
    list_users_uc,
    get_user_uc,
    create_user_uc,
    update_user_uc,
    delete_user_uc,
    update_user_privacy_uc,
)

logger = logging.getLogger(__name__)
users_router = APIRouter()


@users_router.get("")
def get_users():
    try:
        return list_users_uc.execute()
    except Exception as e:
        logger.exception("Failed to list users")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.get("/me")
def get_current_user_me(authorization: Optional[str] = Header(None)):
    if authorization:
        token = authorization.replace("Bearer ", "")
        from domain.services.auth_service import AuthService
        auth_service = AuthService(secret_key=os.environ.get("JWT_SECRET_KEY", "padel-pro-secret-key-change-in-production"))
        payload = auth_service.decode_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                try:
                    return get_user_uc.execute(user_id)
                except Exception as e:
                    raise HTTPException(status_code=404, detail=str(e))
    raise HTTPException(status_code=401, detail="Not authenticated")


@users_router.get("/{user_id}")
def get_user(user_id: str):
    try:
        return get_user_uc.execute(user_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@users_router.post("")
def create_user(user: dict, payload: dict = Depends(require_admin)):
    try:
        return create_user_uc.execute(user)
    except Exception as e:
        logger.exception("Failed to create user")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.put("/{user_id}")
def update_user(user_id: str, user: dict, payload: dict = Depends(require_admin)):
    try:
        return update_user_uc.execute(user_id, user)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@users_router.delete("/{user_id}")
def delete_user(user_id: str, payload: dict = Depends(require_admin)):
    try:
        return delete_user_uc.execute(user_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@users_router.put("/{user_id}/privacy")
def update_user_privacy(user_id: str, privacy: dict, payload: dict = Depends(get_current_user)):
    try:
        return update_user_privacy_uc.execute(user_id, privacy)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
