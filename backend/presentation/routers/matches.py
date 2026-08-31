"""Matches router."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy import text
import json

from infrastructure.database import engine
from presentation.deps_module import require_admin
from domain.services.privacy_service import PrivacyService
from domain.value_objects.privacy_settings import PrivacySettings

matches_router = APIRouter()
privacy_service = PrivacyService()


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


def _apply_privacy_to_matches(matches, conn):
    user_ids = set()
    for m in matches:
        for uid in [
            m.get("playerA1Id"), m.get("playerA2Id"),
            m.get("playerB1Id"), m.get("playerB2Id"),
        ]:
            if uid:
                user_ids.add(uid)
    privacy_map = {}
    for uid in user_ids:
        privacy_map[uid] = _get_privacy(conn, uid)
    result = []
    for m in matches:
        mm = dict(m)
        for prefix in ["playerA1", "playerA2", "playerB1", "playerB2"]:
            uid = m.get(f"{prefix}Id")
            if not uid:
                continue
            priv = privacy_map.get(uid, {})
            if priv and not priv.is_profile_public():
                mm[f"{prefix}Name"] = "Usuario Privado"
                mm[f"{prefix}Avatar"] = ""
        result.append(mm)
    return result


@matches_router.get("")
def get_matches():
    with engine.connect() as conn:
        try:
            result = conn.execute(text("""
                SELECT m.id,
                    m.tournament_id AS tournamentId,
                    m.round_id AS roundId,
                    m.business_id AS businessId,
                    m.court_id AS courtId,
                    m.created_by AS createdBy,
                    m.pair_a_id AS pairAId,
                    m.pair_b_id AS pairBId,
                    m.date_time AS dateTime,
                    m.status,
                    m.visibility,
                    m.sets,
                    m.current_set_index AS currentSetIndex,
                    m.winner_pair_id AS winnerPairId,
                    m.winner_team AS winnerTeam,
                    m.start_time_ms AS startTimeMs,
                    m.elapsed_time_sec AS elapsedTimeSec,
                    m.golden_point AS goldenPoint,
                    m.sets_to_win AS setsToWin,
                    m.round_name AS roundName,
                    m.created_at AS createdAt,
                    m.updated_at AS updatedAt,
                    m.deleted_at AS deletedAt,
                    t.name AS tournamentName,
                    c.name AS courtName,
                    pa.name AS pairAName,
                    pb.name AS pairBName,
                    ua1.name AS playerA1Name,
                    ua2.name AS playerA2Name,
                    ub1.name AS playerB1Name,
                    ub2.name AS playerB2Name,
                    ua1.avatar AS playerA1Avatar,
                    ua2.avatar AS playerA2Avatar,
                    ub1.avatar AS playerB1Avatar,
                    ub2.avatar AS playerB2Avatar
                FROM matches m
                LEFT JOIN tournaments t ON m.tournament_id = t.id
                LEFT JOIN courts c ON m.court_id = c.id
                LEFT JOIN pairs pa ON m.pair_a_id = pa.id
                LEFT JOIN pairs pb ON m.pair_b_id = pb.id
                LEFT JOIN users ua1 ON pa.player1_id = ua1.id
                LEFT JOIN users ua2 ON pa.player2_id = ua2.id
                LEFT JOIN users ub1 ON pb.player1_id = ub1.id
                LEFT JOIN users ub2 ON pb.player2_id = ub2.id
                ORDER BY m.date_time
            """))
        except Exception:
            result = conn.execute(text("""
                SELECT m.id,
                    m.tournament_id AS tournamentId,
                    m.court_id AS courtId,
                    m.created_by AS createdBy,
                    m.pair_a_id AS pairAId,
                    m.pair_b_id AS pairBId,
                    m.date_time AS dateTime,
                    m.status,
                    m.sets,
                    m.created_at AS createdAt,
                    m.updated_at AS updatedAt,
                    t.name AS tournamentName,
                    c.name AS courtName,
                    pa.name AS pairAName,
                    pb.name AS pairBName,
                    ua1.name AS playerA1Name,
                    ua2.name AS playerA2Name,
                    ub1.name AS playerB1Name,
                    ub2.name AS playerB2Name,
                    ua1.avatar AS playerA1Avatar,
                    ua2.avatar AS playerA2Avatar,
                    ub1.avatar AS playerB1Avatar,
                    ub2.avatar AS playerB2Avatar
                FROM matches m
                LEFT JOIN tournaments t ON m.tournament_id = t.id
                LEFT JOIN courts c ON m.court_id = c.id
                LEFT JOIN pairs pa ON m.pair_a_id = pa.id
                LEFT JOIN pairs pb ON m.pair_b_id = pb.id
                LEFT JOIN users ua1 ON pa.player1_id = ua1.id
                LEFT JOIN users ua2 ON pa.player2_id = ua2.id
                LEFT JOIN users ub1 ON pb.player1_id = ub1.id
                LEFT JOIN users ub2 ON pb.player2_id = ub2.id
                ORDER BY m.date_time
            """))
        matches = []
        for row in result.mappings():
            m = dict(row)
            if isinstance(m.get("sets"), str):
                m["sets"] = json.loads(m["sets"])
            m.setdefault("roundId", None)
            m.setdefault("businessId", None)
            m.setdefault("visibility", "PRIVATE")
            m.setdefault("currentSetIndex", 0)
            m.setdefault("winnerPairId", None)
            m.setdefault("winnerTeam", None)
            m.setdefault("startTimeMs", None)
            m.setdefault("elapsedTimeSec", 0)
            m.setdefault("goldenPoint", 0)
            m.setdefault("setsToWin", 2)
            m.setdefault("roundName", None)
            m.setdefault("deletedAt", None)
            m.setdefault("playerA1Name", m.get("playerA1Name") or "Jugador 1")
            m.setdefault("playerA2Name", m.get("playerA2Name") or "Jugador 2")
            m.setdefault("playerB1Name", m.get("playerB1Name") or "Jugador 3")
            m.setdefault("playerB2Name", m.get("playerB2Name") or "Jugador 4")
            m.setdefault("playerA1Avatar", m.get("playerA1Avatar") or "")
            m.setdefault("playerA2Avatar", m.get("playerA2Avatar") or "")
            m.setdefault("playerB1Avatar", m.get("playerB1Avatar") or "")
            m.setdefault("playerB2Avatar", m.get("playerB2Avatar") or "")
            m.setdefault("pairAName", m.get("pairAName") or "Pareja A")
            m.setdefault("pairBName", m.get("pairBName") or "Pareja B")
            m.setdefault("courtName", m.get("courtName") or "Pista por definir")
            m["current_game"] = {}
            matches.append(m)
        return _apply_privacy_to_matches(matches, conn)


@matches_router.get("/{match_id}")
def get_match(match_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT m.id,
                m.tournament_id AS tournamentId,
                m.round_id AS roundId,
                m.business_id AS businessId,
                m.court_id AS courtId,
                m.created_by AS createdBy,
                m.pair_a_id AS pairAId,
                m.pair_b_id AS pairBId,
                m.date_time AS dateTime,
                m.status,
                m.visibility,
                m.sets,
                m.current_set_index AS currentSetIndex,
                m.winner_pair_id AS winnerPairId,
                m.winner_team AS winnerTeam,
                m.start_time_ms AS startTimeMs,
                m.elapsed_time_sec AS elapsedTimeSec,
                m.golden_point AS goldenPoint,
                m.sets_to_win AS setsToWin,
                m.round_name AS roundName,
                m.created_at AS createdAt,
                m.updated_at AS updatedAt,
                m.deleted_at AS deletedAt,
                t.name AS tournamentName,
                c.name AS courtName,
                pa.name AS pairAName,
                pb.name AS pairBName,
                ua1.name AS playerA1Name,
                ua2.name AS playerA2Name,
                ub1.name AS playerB1Name,
                ub2.name AS playerB2Name,
                ua1.avatar AS playerA1Avatar,
                ua2.avatar AS playerA2Avatar,
                ub1.avatar AS playerB1Avatar,
                ub2.avatar AS playerB2Avatar
            FROM matches m
            LEFT JOIN tournaments t ON m.tournament_id = t.id
            LEFT JOIN courts c ON m.court_id = c.id
            LEFT JOIN pairs pa ON m.pair_a_id = pa.id
            LEFT JOIN pairs pb ON m.pair_b_id = pb.id
            LEFT JOIN users ua1 ON pa.player1_id = ua1.id
            LEFT JOIN users ua2 ON pa.player2_id = ua2.id
            LEFT JOIN users ub1 ON pb.player1_id = ub1.id
            LEFT JOIN users ub2 ON pb.player2_id = ub2.id
            WHERE m.id = :id
        """), {"id": match_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Match not found")
        m = dict(row)
        if isinstance(m.get("sets"), str):
            m["sets"] = json.loads(m["sets"])
        m.setdefault("roundId", None)
        m.setdefault("businessId", None)
        m.setdefault("visibility", "PRIVATE")
        m.setdefault("currentSetIndex", 0)
        m.setdefault("winnerPairId", None)
        m.setdefault("winnerTeam", None)
        m.setdefault("startTimeMs", None)
        m.setdefault("elapsedTimeSec", 0)
        m.setdefault("goldenPoint", 0)
        m.setdefault("setsToWin", 2)
        m.setdefault("roundName", None)
        m.setdefault("deletedAt", None)
        m.setdefault("playerA1Name", m.get("playerA1Name") or "Jugador 1")
        m.setdefault("playerA2Name", m.get("playerA2Name") or "Jugador 2")
        m.setdefault("playerB1Name", m.get("playerB1Name") or "Jugador 3")
        m.setdefault("playerB2Name", m.get("playerB2Name") or "Jugador 4")
        m.setdefault("playerA1Avatar", m.get("playerA1Avatar") or "")
        m.setdefault("playerA2Avatar", m.get("playerA2Avatar") or "")
        m.setdefault("playerB1Avatar", m.get("playerB1Avatar") or "")
        m.setdefault("playerB2Avatar", m.get("playerB2Avatar") or "")
        m.setdefault("pairAName", m.get("pairAName") or "Pareja A")
        m.setdefault("pairBName", m.get("pairBName") or "Pareja B")
        m.setdefault("courtName", m.get("courtName") or "Pista por definir")
        m["current_game"] = {}
        return _apply_privacy_to_matches([m], conn)[0]


@matches_router.get("/{match_id}/players")
def get_match_players(match_id: str):
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT mp.*, u.name, u.surname, u.avatar, p.name as pair_name
            FROM match_players mp
            JOIN users u ON mp.user_id = u.id
            JOIN pairs p ON mp.pair_id = p.id
            WHERE mp.match_id = :mid
        """), {"mid": match_id}).mappings().all()
        return [dict(r) for r in rows]


@matches_router.post("")
def create_match(match: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO matches (id, tournament_id, round_id, business_id, court_id, created_by,
                pair_a_id, pair_b_id, date_time, status, visibility, sets, current_set_index,
                winner_pair_id, winner_team, start_time_ms, elapsed_time_sec, golden_point,
                sets_to_win, round_name)
            VALUES (:id, :tournament_id, :round_id, :business_id, :court_id, :created_by,
                :pair_a_id, :pair_b_id, :date_time, :status, :visibility, :sets, :current_set_index,
                :winner_pair_id, :winner_team, :start_time_ms, :elapsed_time_sec, :golden_point,
                :sets_to_win, :round_name)
            ON DUPLICATE KEY UPDATE
                tournament_id = VALUES(tournament_id), court_id = VALUES(court_id),
                date_time = VALUES(date_time), pair_a_id = VALUES(pair_a_id),
                pair_b_id = VALUES(pair_b_id), status = VALUES(status),
                sets = VALUES(sets), current_set_index = VALUES(current_set_index),
                winner_pair_id = VALUES(winner_pair_id), winner_team = VALUES(winner_team),
                start_time_ms = VALUES(start_time_ms), elapsed_time_sec = VALUES(elapsed_time_sec),
                golden_point = VALUES(golden_point), sets_to_win = VALUES(sets_to_win),
                round_name = VALUES(round_name)
        """), {
            "id": match["id"],
            "tournament_id": match.get("tournament_id"),
            "round_id": match.get("round_id"),
            "business_id": match.get("business_id"),
            "court_id": match.get("court_id"),
            "created_by": match.get("created_by", ""),
            "pair_a_id": match.get("pair_a_id") or match.get("pairAId"),
            "pair_b_id": match.get("pair_b_id") or match.get("pairBId"),
            "date_time": match.get("date_time") or match.get("dateTime"),
            "status": match.get("status", "SCHEDULED"),
            "visibility": match.get("visibility", "PRIVATE"),
            "sets": json.dumps(match.get("sets", [])),
            "current_set_index": match.get("current_set_index", 0),
            "winner_pair_id": match.get("winner_pair_id") or match.get("winnerPairId"),
            "winner_team": match.get("winner_team") or match.get("winnerTeam"),
            "start_time_ms": match.get("start_time_ms") or match.get("startTimeMs"),
            "elapsed_time_sec": match.get("elapsed_time_sec", 0),
            "golden_point": 1 if match.get("golden_point") else 0,
            "sets_to_win": match.get("sets_to_win", 2),
            "round_name": match.get("round_name") or match.get("roundName"),
        })
    return match


@matches_router.put("/{match_id}/court")
def update_match_court(match_id: str, body: dict):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE matches SET court_id = :court_id, court_name = :court_name
            WHERE id = :id
        """), {
            "id": match_id,
            "court_id": body.get("courtId") or body.get("court_id"),
            "court_name": body.get("courtName") or body.get("court_name"),
        })
    return {"status": "updated"}


@matches_router.post("/{match_id}/finish")
def finish_match(match_id: str, body: dict):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE matches SET status = 'FINISHED', winner_pair_id = :winner_id, winner_team = :winner_team
            WHERE id = :id
        """), {
            "id": match_id,
            "winner_id": body.get("winnerPairId") or body.get("winner_pair_id"),
            "winner_team": body.get("winnerTeam") or body.get("winner_team"),
        })
    return {"status": "finished"}


@matches_router.post("/{match_id}/events")
def create_match_event(match_id: str, event: dict):
    event_id = event.get("id") or f"event_{match_id}_{event.get('set_number', 0)}_{event.get('game_number', 0)}"
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO match_events (id, match_id, set_number, game_number, event_type,
                description, score_snapshot)
            VALUES (:id, :match_id, :set_number, :game_number, :event_type, :description, :score_snapshot)
            ON DUPLICATE KEY UPDATE
                event_type = VALUES(event_type), description = VALUES(description)
        """), {
            "id": event_id,
            "match_id": match_id,
            "set_number": event.get("set_number", 0),
            "game_number": event.get("game_number"),
            "event_type": event.get("event_type", "POINT"),
            "description": event.get("description"),
            "score_snapshot": json.dumps(event.get("score_snapshot")) if event.get("score_snapshot") else None,
        })
    return event


@matches_router.delete("/{match_id}")
def delete_match(match_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("UPDATE matches SET deleted_at = NOW() WHERE id = :id"), {"id": match_id})
    return {"message": "Match deleted"}
