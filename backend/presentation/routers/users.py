"""Users router."""

from fastapi import APIRouter, Depends, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional, List
import os
import json
from sqlalchemy import text
from jose import jwt, JWTError
from datetime import datetime

from infrastructure.database import engine
from domain.services.auth_service import AuthService
from domain.services.privacy_service import PrivacyService
from domain.value_objects.privacy_settings import PrivacySettings

users_router = APIRouter()

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "padel-pro-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
auth_service = AuthService(secret_key=JWT_SECRET_KEY)
privacy_service = PrivacyService()


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
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


def _get_privacy(conn, user_id: str) -> PrivacySettings:
    try:
        row = conn.execute(text("""
            SELECT profile_visibility, points_visibility, games_visibility, tournaments_visibility
            FROM privacy_settings WHERE user_id = :uid
        """), {"uid": user_id}).mappings().first()
        if row:
            return PrivacySettings(
                user_id=user_id,
                profile_visibility=row["profile_visibility"],
                points_visibility=row["points_visibility"],
                games_visibility=row["games_visibility"],
                tournaments_visibility=row["tournaments_visibility"],
            )
    except Exception:
        pass
    return PrivacySettings(user_id=user_id)


def _build_user_response(user: dict, role_name: Optional[str] = None) -> dict:
    level = user.get("level") or "Intermedio"
    position = user.get("position") or "Drive (Derecha)"
    dominant_hand = user.get("dominant_hand") or "Derecha"
    stats = user.get("stats")
    if not stats:
        stats = {}
    return {
        "id": user.get("id"),
        "name": user.get("name") or "",
        "surname": user.get("surname") or "",
        "username": user.get("username") or "",
        "email": user.get("email") or "",
        "avatar": user.get("avatar") or "",
        "level": level,
        "position": position,
        "dominant_hand": dominant_hand,
        "points": user.get("points") or 0,
        "stats": stats,
        "role": role_name or "PLAYER",
        "account_type": user.get("account_type") or "USER",
        "status": user.get("status") or "ACTIVE",
        "invitation_code": user.get("invitation_code"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
        "phone": None,
        "current_pair_id": None,
        "partner_name": None,
    }


@users_router.get("")
def get_users():
    with engine.connect() as conn:
        try:
            result = conn.execute(text("""
                SELECT u.*, ua.email as auth_email,
                       (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                FROM users u
                LEFT JOIN users_auth ua ON u.id = ua.user_id
                WHERE u.deleted_at IS NULL
                ORDER BY u.points DESC
            """))
        except Exception:
            result = conn.execute(text("""
                SELECT u.*, ua.email as auth_email,
                       (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                FROM users u
                LEFT JOIN users_auth ua ON u.id = ua.user_id
                ORDER BY u.points DESC
            """))
        users = []
        for row in result.mappings():
            user = dict(row)
            resp = _build_user_response(user, user.get("role_name"))
            privacy = _get_privacy(conn, user.get("id"))
            users.append(privacy_service.apply_user_privacy(resp, privacy, viewer_is_self=False))
        return users


@users_router.get("/me")
def get_current_user_me(authorization: Optional[str] = Header(None)):
    if authorization:
        token = authorization.replace("Bearer ", "")
        payload = auth_service.decode_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                with engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT u.*, ua.email as auth_email,
                               (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                        FROM users u
                        LEFT JOIN users_auth ua ON u.id = ua.user_id
                        WHERE u.id = :id
                    """), {"id": user_id})
                    row = result.mappings().first()
                    if row:
                        user = dict(row)
                        resp = _build_user_response(user, user.get("role_name"))
                        privacy = _get_privacy(conn, user_id)
                        return privacy_service.apply_user_privacy(resp, privacy, viewer_is_self=True)
    raise HTTPException(status_code=401, detail="Not authenticated")


@users_router.get("/{user_id}")
def get_user(user_id: str):
    with engine.connect() as conn:
        try:
            result = conn.execute(text("""
                SELECT u.*, ua.email as auth_email,
                       (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                FROM users u
                LEFT JOIN users_auth ua ON u.id = ua.user_id
                WHERE u.id = :id AND u.deleted_at IS NULL
            """), {"id": user_id})
        except Exception:
            result = conn.execute(text("""
                SELECT u.*, ua.email as auth_email,
                       (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                FROM users u
                LEFT JOIN users_auth ua ON u.id = ua.user_id
                WHERE u.id = :id
            """), {"id": user_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        user = dict(row)
        resp = _build_user_response(user, user.get("role_name"))
        privacy = _get_privacy(conn, user_id)
        return privacy_service.apply_user_privacy(resp, privacy, viewer_is_self=False)


@users_router.post("")
def create_user(user: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO users (id, name, surname, username, email, avatar, account_type, status,
                level, position, dominant_hand, points)
            VALUES (:id, :name, :surname, :username, :email, :avatar, 'USER', 'ACTIVE',
                :level, :position, :dominant_hand, :points)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), surname = VALUES(surname), username = VALUES(username),
                email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level),
                position = VALUES(position), dominant_hand = VALUES(dominant_hand),
                points = VALUES(points)
        """), {
            "id": user["id"], "name": user["name"], "surname": user.get("surname", ""),
            "username": user["username"], "email": user.get("email"),
            "avatar": user.get("avatar"), "level": user.get("level"),
            "position": user.get("position"), "dominant_hand": user.get("dominant_hand"),
            "points": user.get("points", 0),
        })

        if user.get("email"):
            hashed = auth_service.hash_password(user.get("password") or "password")
            conn.execute(text("""
                INSERT INTO users_auth (user_id, email, hashed_password)
                VALUES (:user_id, :email, :hashed_password)
                ON DUPLICATE KEY UPDATE email = VALUES(email), hashed_password = VALUES(hashed_password)
            """), {
                "user_id": user["id"],
                "email": user["email"],
                "hashed_password": hashed,
            })
    return user


@users_router.put("/{user_id}")
def update_user(user_id: str, user: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE users SET
                name = :name, surname = :surname, username = :username, email = :email,
                avatar = :avatar, level = :level, position = :position,
                dominant_hand = :dominant_hand, points = :points
            WHERE id = :id
        """), {
            "id": user_id, "name": user.get("name"), "surname": user.get("surname", ""),
            "username": user.get("username"), "email": user.get("email"),
            "avatar": user.get("avatar"), "level": user.get("level"),
            "position": user.get("position"), "dominant_hand": user.get("dominant_hand"),
            "points": user.get("points", 0),
        })
    return {"id": user_id, **user}


@users_router.delete("/{user_id}")
def delete_user(user_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        try:
            conn.execute(text("UPDATE users SET deleted_at = NOW() WHERE id = :id"), {"id": user_id})
            return {"message": "User soft-deleted"}
        except Exception:
            pass
        
        try:
            conn.execute(text("DELETE FROM user_roles WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM profiles WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM privacy_settings WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM business_users WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM user_points WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM notifications WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM audit_logs WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM tournament_players WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM match_players WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("UPDATE pairs SET player1_id = NULL WHERE player1_id = :id"), {"id": user_id})
            conn.execute(text("UPDATE pairs SET player2_id = NULL WHERE player2_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM users_auth WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
            return {"message": "User deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}")
