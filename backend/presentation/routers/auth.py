"""Auth router."""

from fastapi import APIRouter, Depends, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional
import os
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy import text

from infrastructure.database import engine
from domain.services.auth_service import AuthService

auth_router = APIRouter()

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "padel-pro-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
auth_service = AuthService(secret_key=JWT_SECRET_KEY)


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

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users_auth WHERE email = :email"),
            {"email": body.email}
        )
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        auth_user = dict(row)
        if not bcrypt.checkpw(body.password.encode("utf-8"), auth_user["hashed_password"].encode("utf-8")):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = auth_user.get("user_id") or auth_user.get("id")
        role_row = conn.execute(text("""
            SELECT r.name FROM user_roles ur
            JOIN roles r ON ur.role_id = r.id
            WHERE ur.user_id = :uid
            ORDER BY CASE r.name
                WHEN 'SUPER_ADMIN' THEN 1
                WHEN 'BUSINESS_ADMIN' THEN 2
                WHEN 'BUSINESS_MANAGER' THEN 3
                WHEN 'ADMIN' THEN 4
                WHEN 'USER' THEN 5
                ELSE 6
            END
            LIMIT 1
        """), {"uid": user_id}).mappings().first()
        role = role_row["name"] if role_row else "PLAYER"

        try:
            conn.execute(
                text("UPDATE users_auth SET last_login = :now WHERE user_id = :uid"),
                {"now": datetime.utcnow(), "uid": user_id}
            )
        except Exception:
            pass

        token = auth_service.create_access_token(user_id, role)
        return TokenResponse(access_token=token, token_type="bearer", user_id=user_id, role=role)


@auth_router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest):
    email = body.email
    password = body.password
    name = body.name
    role = body.role

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT user_id FROM users_auth WHERE email = :email"),
            {"email": email}
        )
        if result.mappings().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        user_id = "usr_" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
        hashed = auth_service.hash_password(password)

        conn.execute(text("""
            INSERT INTO users (id, name, surname, username, email, avatar, account_type, status,
                level, position, dominant_hand, points)
            VALUES (:id, :name, :surname, :username, :email, :avatar, 'USER', 'ACTIVE',
                :level, :position, :dominant_hand, :points)
        """), {
            "id": user_id, "name": name, "surname": body.surname,
            "username": body.username or email.split("@")[0],
            "email": email, "avatar": None,
            "level": None, "position": None, "dominant_hand": None,
            "points": 0,
        })

        conn.execute(text("""
            INSERT INTO users_auth (user_id, email, hashed_password)
            VALUES (:user_id, :email, :hashed_password)
        """), {"user_id": user_id, "email": email, "hashed_password": hashed})

        role_row = conn.execute(
            text("SELECT id FROM roles WHERE name = :name"),
            {"name": role}
        ).mappings().first()
        role_id = role_row["id"] if role_row else conn.execute(
            text("INSERT INTO roles (name) VALUES (:name)"),
            {"name": role}
        ).lastrowid
        conn.execute(
            text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"),
            {"user_id": user_id, "role_id": role_id}
        )

    token = auth_service.create_access_token(user_id, role)
    return TokenResponse(access_token=token, token_type="bearer", user_id=user_id, role=role)
