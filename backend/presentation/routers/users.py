"""Users router."""

import logging
import os
from fastapi import APIRouter, Depends, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional, List

from presentation.deps_module import (
    get_current_user,
    require_admin,
    require_super_admin,
    list_users_uc,
    get_user_uc,
    create_user_uc,
    update_user_uc,
    delete_user_uc,
    update_user_privacy_uc,
    convert_guest_uc,
)

logger = logging.getLogger(__name__)
users_router = APIRouter()


@users_router.get("")
def get_users(payload: dict = Depends(get_current_user)):
    try:
        role = payload.get("role", "PLAYER")
        user_id = payload.get("sub")
        return list_users_uc.execute(current_user_id=user_id, current_role=role)
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
                    return get_user_uc.execute(user_id, viewer_is_self=True)
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
def create_user(user: dict, payload: dict = Depends(require_super_admin)):
    try:
        user.setdefault("role", "USER")
        return create_user_uc.execute(user, created_by_role=payload.get("role", "SUPER_ADMIN"))
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
def delete_user(user_id: str, payload: dict = Depends(get_current_user)):
    try:
        current_user_id = payload.get("sub")
        current_role = payload.get("role", "PLAYER")
        ADMIN_ROLES = {"ADMIN", "SUPER_ADMIN", "BUSINESS_ADMIN", "BUSINESS_MANAGER"}
        if current_role not in ADMIN_ROLES:
            raise HTTPException(status_code=403, detail="Admin access required")
        return delete_user_uc.execute(user_id, current_user_id=current_user_id, current_role=current_role)
    except EntityNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except ValidationError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.exception("Failed to delete user")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.put("/{user_id}/privacy")
def update_user_privacy(user_id: str, privacy: dict, payload: dict = Depends(get_current_user)):
    try:
        return update_user_privacy_uc.execute(user_id, privacy)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ConvertGuestRequest(BaseModel):
    invitation_code: str
    password: str
    name: str = ""
    surname: str = ""
    username: str = ""


@users_router.post("/convert-guest")
def convert_guest(body: ConvertGuestRequest):
    try:
        return convert_guest_uc.execute(body.invitation_code, body.password, {
            "name": body.name,
            "surname": body.surname,
            "username": body.username,
        })
    except EntityNotFound:
        raise HTTPException(status_code=404, detail="Invalid invitation code")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Failed to convert guest")
        raise HTTPException(status_code=500, detail=str(e))
