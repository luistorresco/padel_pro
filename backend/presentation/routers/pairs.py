"""Pairs router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from sqlalchemy import text

from infrastructure.database import engine
from domain.services.auth_service import AuthService
from domain.services.privacy_service import PrivacyService
from domain.value_objects.privacy_settings import PrivacySettings
from presentation.deps_module import get_current_user, require_admin

pairs_router = APIRouter()


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


@pairs_router.get("")
def get_pairs():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT p.*, u1.name as player1_name, u2.name as player2_name,
                   u1.avatar as player1_avatar, u2.avatar as player2_avatar,
                   u1.level as p1_level, u2.level as p2_level,
                   u1.points as p1_points, u2.points as p2_points
            FROM pairs p
            LEFT JOIN users u1 ON p.player1_id = u1.id
            LEFT JOIN users u2 ON p.player2_id = u2.id
            ORDER BY p.created_at
        """))
        pairs = []
        for row in result.mappings():
            pair = dict(row)
            pairs.append({
                "id": pair["id"],
                "name": pair.get("name"),
                "status": pair.get("status", "ACTIVE"),
                "player1Id": pair["player1_id"],
                "player2Id": pair["player2_id"],
                "player1Name": pair.get("player1_name") or "",
                "player2Name": pair.get("player2_name") or "",
                "player1Avatar": pair.get("player1_avatar") or "",
                "player2Avatar": pair.get("player2_avatar") or "",
                "p1Level": pair.get("p1_level") or "Intermedio",
                "p2Level": pair.get("p2_level") or "Intermedio",
                "p1Points": pair.get("p1_points") or 0,
                "p2Points": pair.get("p2_points") or 0,
                "tournamentsDisputed": pair.get("tournaments_disputed", 0),
                "titlesWon": pair.get("titles_won", 0),
                "createdAt": pair.get("created_at"),
            })
        return pairs


@pairs_router.get("/{pair_id}")
def get_pair(pair_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT p.*, u1.name as player1_name, u2.name as player2_name,
                   u1.avatar as player1_avatar, u2.avatar as player2_avatar,
                   u1.level as p1_level, u2.level as p2_level,
                   u1.points as p1_points, u2.points as p2_points
            FROM pairs p
            LEFT JOIN users u1 ON p.player1_id = u1.id
            LEFT JOIN users u2 ON p.player2_id = u2.id
            WHERE p.id = :id
        """), {"id": pair_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Pair not found")
        pair = dict(row)
        return {
            "id": pair["id"],
            "name": pair.get("name"),
            "status": pair.get("status", "ACTIVE"),
            "player1Id": pair["player1_id"],
            "player2Id": pair["player2_id"],
            "player1Name": pair.get("player1_name") or "",
            "player2Name": pair.get("player2_name") or "",
            "player1Avatar": pair.get("player1_avatar") or "",
            "player2Avatar": pair.get("player2_avatar") or "",
            "p1Level": pair.get("p1_level") or "Intermedio",
            "p2Level": pair.get("p2_level") or "Intermedio",
            "p1Points": pair.get("p1_points") or 0,
            "p2Points": pair.get("p2_points") or 0,
            "tournamentsDisputed": pair.get("tournaments_disputed", 0),
            "titlesWon": pair.get("titles_won", 0),
            "createdAt": pair.get("created_at"),
        }


@pairs_router.post("")
def create_pair(pair: dict, payload: dict = Depends(get_current_user)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO pairs (id, name, player1_id, player2_id, created_by, status,
                tournaments_disputed, titles_won)
            VALUES (:id, :name, :player1_id, :player2_id, :created_by, :status,
                :tournaments_disputed, :titles_won)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id),
                status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed),
                titles_won = VALUES(titles_won)
        """), {
            "id": pair.get("id") or pair.get("player1Id") + "_" + pair.get("player2Id"),
            "name": pair.get("name"),
            "player1_id": pair.get("player1Id") or pair.get("player1_id"),
            "player2_id": pair.get("player2Id") or pair.get("player2_id"),
            "created_by": pair.get("createdBy") or pair.get("created_by") or pair.get("player1Id") or pair.get("player1_id"),
            "status": pair.get("status", "ACTIVE"),
            "tournaments_disputed": pair.get("tournamentsDisputed", pair.get("tournaments_disputed", 0)),
            "titles_won": pair.get("titlesWon", pair.get("titles_won", 0)),
        })
    return pair


@pairs_router.delete("/{pair_id}")
def delete_pair(pair_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM pairs WHERE id = :id"), {"id": pair_id})
    return {"message": "Pair deleted"}
