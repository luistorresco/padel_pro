"""FastAPI dependencies."""

from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from domain.services.auth_service import AuthService

JWT_SECRET_KEY = "padel-pro-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
auth_service = AuthService(secret_key=JWT_SECRET_KEY)


def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


def require_admin(payload: dict = Depends(get_current_user)):
    ADMIN_ROLES = {"ADMIN", "SUPER_ADMIN", "BUSINESS_ADMIN", "BUSINESS_MANAGER"}
    if payload.get("role") not in ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload
