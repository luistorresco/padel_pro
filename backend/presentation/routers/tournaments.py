"""Tournaments router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from sqlalchemy import text
import json

from infrastructure.database import engine
from presentation.deps_module import require_admin

tournaments_router = APIRouter()


def _build_tournament_response(t: dict) -> dict:
    return {
        "id": t["id"],
        "name": t["name"],
        "created_by": t["created_by"],
        "start_date": t.get("start_date"),
        "end_date": t.get("end_date"),
        "status": t.get("status", "DRAFT"),
        "business_id": t.get("business_id"),
        "logo": t.get("logo"),
        "description": t.get("description"),
        "category": t.get("category"),
        "level": t.get("level"),
        "location": t.get("location"),
        "format": t.get("format"),
        "max_pairs": t.get("max_pairs"),
        "visibility": t.get("visibility", "PRIVATE"),
        "rules": t.get("rules") or {},
        "created_at": t.get("created_at"),
        "updated_at": t.get("updated_at"),
        "deleted_at": t.get("deleted_at"),
    }


@tournaments_router.get("")
def get_tournaments():
    with engine.connect() as conn:
        try:
            result = conn.execute(text("SELECT * FROM tournaments WHERE deleted_at IS NULL ORDER BY start_date"))
        except Exception:
            result = conn.execute(text("SELECT * FROM tournaments ORDER BY start_date"))
        tournaments = []
        for row in result.mappings():
            t = dict(row)
            t["registered_pair_ids"] = [r["pair_id"] for r in conn.execute(
                text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"),
                {"tid": t["id"]}
            ).mappings()]
            t["registered_user_ids"] = [r["user_id"] for r in conn.execute(
                text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"),
                {"tid": t["id"]}
            ).mappings()]
            tournaments.append(_build_tournament_response(t))
        return tournaments


@tournaments_router.get("/{tournament_id}")
def get_tournament(tournament_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Tournament not found")
        t = dict(row)
        t["registered_pair_ids"] = [r["pair_id"] for r in conn.execute(
            text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"),
            {"tid": tournament_id}
        ).mappings()]
        t["registered_user_ids"] = [r["user_id"] for r in conn.execute(
            text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"),
            {"tid": tournament_id}
        ).mappings()]
        return _build_tournament_response(t)


@tournaments_router.get("/{tournament_id}/full")
def get_tournament_full(tournament_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Tournament not found")
        t = dict(row)

        categories = conn.execute(
            text("SELECT * FROM tournament_categories WHERE tournament_id = :tid"),
            {"tid": tournament_id}
        ).mappings().all()

        rounds = conn.execute(
            text("SELECT * FROM tournament_rounds WHERE tournament_id = :tid"),
            {"tid": tournament_id}
        ).mappings().all()

        pairs = conn.execute(text("""
            SELECT tp.*, p.player1_id, p.player2_id, p.name as pair_name,
                   u1.name as player1_name, u2.name as player2_name,
                   u1.avatar as player1_avatar, u2.avatar as player2_avatar
            FROM tournament_pairs tp
            JOIN pairs p ON tp.pair_id = p.id
            LEFT JOIN users u1 ON p.player1_id = u1.id
            LEFT JOIN users u2 ON p.player2_id = u2.id
            WHERE tp.tournament_id = :tid
        """), {"tid": tournament_id}).mappings().all()

        players = conn.execute(text("""
            SELECT tp.*, u.name, u.surname, u.avatar, u.level, u.points
            FROM tournament_players tp
            JOIN users u ON tp.user_id = u.id
            WHERE tp.tournament_id = :tid
        """), {"tid": tournament_id}).mappings().all()

        matches = conn.execute(text("""
            SELECT m.*, t.name as tournament_name, c.name as court_name,
                   pa.name as pair_a_name, pb.name as pair_b_name,
                   ua1.name as player_a1_name, ua2.name as player_a2_name,
                   ub1.name as player_b1_name, ub2.name as player_b2_name,
                   ua1.avatar as player_a1_avatar, ua2.avatar as player_a2_avatar,
                   ub1.avatar as player_b1_avatar, ub2.avatar as player_b2_avatar
            FROM matches m
            LEFT JOIN tournaments t ON m.tournament_id = t.id
            LEFT JOIN courts c ON m.court_id = c.id
            LEFT JOIN pairs pa ON m.pair_a_id = pa.id
            LEFT JOIN pairs pb ON m.pair_b_id = pb.id
            LEFT JOIN users ua1 ON pa.player1_id = ua1.id
            LEFT JOIN users ua2 ON pa.player2_id = ua2.id
            LEFT JOIN users ub1 ON pb.player1_id = ub1.id
            LEFT JOIN users ub2 ON pb.player2_id = ub2.id
            WHERE m.tournament_id = :tid
            ORDER BY m.date_time
        """), {"tid": tournament_id}).mappings().all()

        return {
            **_build_tournament_response(t),
            "categories": [dict(c) for c in categories],
            "rounds": [dict(r) for r in rounds],
            "pairs": [dict(p) for p in pairs],
            "players": [dict(p) for p in players],
            "matches": [dict(m) for m in matches],
        }


@tournaments_router.post("")
def create_tournament(tournament: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO tournaments (id, business_id, created_by, name, logo, description,
                category, level, location, start_date, end_date, status, format, max_pairs,
                visibility, rules)
            VALUES (:id, :business_id, :created_by, :name, :logo, :description,
                :category, :level, :location, :start_date, :end_date, :status, :format, :max_pairs,
                :visibility, :rules)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), description = VALUES(description),
                category = VALUES(category), level = VALUES(level),
                location = VALUES(location), start_date = VALUES(start_date),
                end_date = VALUES(end_date), status = VALUES(status),
                format = VALUES(format), max_pairs = VALUES(max_pairs),
                visibility = VALUES(visibility), rules = VALUES(rules)
        """), {
            "id": tournament["id"],
            "business_id": tournament.get("business_id"),
            "created_by": tournament.get("created_by", ""),
            "name": tournament["name"],
            "logo": tournament.get("logo"),
            "description": tournament.get("description"),
            "category": tournament.get("category"),
            "level": tournament.get("level"),
            "location": tournament.get("location"),
            "start_date": tournament.get("start_date"),
            "end_date": tournament.get("end_date"),
            "status": tournament.get("status", "DRAFT"),
            "format": tournament.get("format"),
            "max_pairs": tournament.get("max_pairs"),
            "visibility": tournament.get("visibility", "PRIVATE"),
            "rules": json.dumps(tournament.get("rules", {})),
        })
    return {**tournament, "id": tournament["id"]}


@tournaments_router.put("/{tournament_id}")
def update_tournament(tournament_id: str, tournament: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Tournament not found")
        conn.execute(text("""
            UPDATE tournaments SET
                name = :name, logo = :logo, description = :description, category = :category,
                level = :level, location = :location, start_date = :start_date, end_date = :end_date,
                status = :status, format = :format, max_pairs = :max_pairs,
                visibility = :visibility, rules = :rules
            WHERE id = :id
        """), {
            "id": tournament_id,
            "name": tournament.get("name"), "logo": tournament.get("logo"),
            "description": tournament.get("description"), "category": tournament.get("category"),
            "level": tournament.get("level"), "location": tournament.get("location"),
            "start_date": tournament.get("start_date"), "end_date": tournament.get("end_date"),
            "status": tournament.get("status"), "format": tournament.get("format"),
            "max_pairs": tournament.get("max_pairs"),
            "visibility": tournament.get("visibility", "PRIVATE"),
            "rules": json.dumps(tournament.get("rules", {})),
        })
    return {**tournament, "id": tournament_id}


@tournaments_router.delete("/{tournament_id}")
def delete_tournament(tournament_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("UPDATE tournaments SET deleted_at = NOW() WHERE id = :id"), {"id": tournament_id})
    return {"message": "Tournament deleted"}


@tournaments_router.post("/{tournament_id}/register")
def register_for_tournament(tournament_id: str, body: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Tournament not found")

        pair_id = body.get("pairId") or body.get("pair_id")
        user_id = body.get("userId") or body.get("user_id")
        court_id = body.get("courtId") or body.get("court_id")
        date_time = body.get("dateTime") or body.get("date_time")

        if pair_id:
            conn.execute(text("""
                INSERT INTO tournament_pairs (tournament_id, pair_id, status)
                VALUES (:tid, :pid, 'REGISTERED')
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """), {"tid": tournament_id, "pid": pair_id})

        if user_id:
            conn.execute(text("""
                INSERT INTO tournament_players (tournament_id, user_id, status)
                VALUES (:tid, :uid, 'REGISTERED')
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """), {"tid": tournament_id, "uid": user_id})

        if pair_id and court_id and date_time:
            match_id = f"match_{tournament_id}_{pair_id}"
            conn.execute(text("""
                INSERT INTO matches (id, tournament_id, pair_a_id, date_time, court_id, status, created_by)
                VALUES (:id, :tid, :pid, :dt, :cid, 'SCHEDULED', :created_by)
                ON DUPLICATE KEY UPDATE court_id = VALUES(court_id), date_time = VALUES(date_time)
            """), {
                "id": match_id, "tid": tournament_id, "pid": pair_id,
                "dt": date_time, "cid": court_id, "created_by": payload.get("sub", ""),
            })

    return {"status": "registered"}
