"""Auth router."""

import os
from fastapi import APIRouter, Depends, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional

from presentation.deps_module import (
    login_uc,
    register_uc,
    get_current_user_uc,
    get_current_user,
    require_admin,
)

auth_router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    surname: str = ""
    username: str = ""
    role: str = "PLAYER"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    role: str


@auth_router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        result = login_uc.execute(body.email, body.password)
        return TokenResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.get("/me")
def auth_me(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    token = authorization.replace("Bearer ", "")
    from domain.services.auth_service import AuthService
    auth_service = AuthService(secret_key=os.environ.get("JWT_SECRET_KEY", "padel-pro-secret-key-change-in-production"))
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        return get_current_user_uc.execute(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@auth_router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest):
    try:
        result = register_uc.execute(body.name, body.surname, body.username, body.email, body.password, body.role)
        return TokenResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
