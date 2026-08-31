"""SQLAlchemy match repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.match import Match
from domain.repositories.match_repository import IMatchRepository


class SQLAlchemyMatchRepository(IMatchRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_id(self, match_id: str) -> Optional[Match]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM matches WHERE id = :id"),
                {"id": match_id}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def save(self, match: Match) -> Match:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO matches (id, tournament_id, round_id, business_id, court_id, created_by,
                    pair_a_id, pair_b_id, date_time, status, visibility, sets, current_set_index,
                    winner_pair_id, winner_team, start_time_ms, elapsed_time_sec, golden_point,
                    sets_to_win, round_name, deleted_at)
                VALUES (:id, :tournament_id, :round_id, :business_id, :court_id, :created_by,
                    :pair_a_id, :pair_b_id, :date_time, :status, :visibility, :sets, :current_set_index,
                    :winner_pair_id, :winner_team, :start_time_ms, :elapsed_time_sec, :golden_point,
                    :sets_to_win, :round_name, :deleted_at)
                ON DUPLICATE KEY UPDATE
                    tournament_id = VALUES(tournament_id), court_id = VALUES(court_id),
                    date_time = VALUES(date_time), pair_a_id = VALUES(pair_a_id),
                    pair_b_id = VALUES(pair_b_id), status = VALUES(status),
                    sets = VALUES(sets), current_set_index = VALUES(current_set_index),
                    winner_pair_id = VALUES(winner_pair_id), winner_team = VALUES(winner_team),
                    start_time_ms = VALUES(start_time_ms), elapsed_time_sec = VALUES(elapsed_time_sec),
                    golden_point = VALUES(golden_point), sets_to_win = VALUES(sets_to_win),
                    round_name = VALUES(round_name), deleted_at = VALUES(deleted_at)
            """), {
                "id": match.id, "tournament_id": match.tournament_id,
                "round_id": match.round_id, "business_id": match.business_id,
                "court_id": match.court_id, "created_by": match.created_by,
                "pair_a_id": match.pair_a_id, "pair_b_id": match.pair_b_id,
                "date_time": match.date_time, "status": match.status,
                "visibility": match.visibility,
                "sets": str(match.sets) if match.sets else None,
                "current_set_index": match.current_set_index,
                "winner_pair_id": match.winner_pair_id, "winner_team": match.winner_team,
                "start_time_ms": match.start_time_ms,
                "elapsed_time_sec": match.elapsed_time_sec,
                "golden_point": 1 if match.golden_point else 0,
                "sets_to_win": match.sets_to_win, "round_name": match.round_name,
                "deleted_at": match.deleted_at,
            })
        return match

    def delete(self, match_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text("UPDATE matches SET deleted_at = NOW() WHERE id = :id"),
                {"id": match_id}
            )

    def list_all(self) -> List[Match]:
        with self.engine.connect() as conn:
            rows = conn.execute(
                text("SELECT * FROM matches WHERE deleted_at IS NULL ORDER BY date_time")
            ).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def find_by_tournament(self, tournament_id: str) -> List[Match]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT * FROM matches WHERE tournament_id = :tid AND deleted_at IS NULL
                ORDER BY date_time
            """), {"tid": tournament_id}).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def find_players(self, match_id: str) -> List[dict]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT mp.*, u.name, u.surname, u.avatar, p.name as pair_name
                FROM match_players mp
                JOIN users u ON mp.user_id = u.id
                JOIN pairs p ON mp.pair_id = p.id
                WHERE mp.match_id = :mid
            """), {"mid": match_id}).mappings().all()
            return [dict(r) for r in rows]

    def _to_entity(self, row: dict) -> Match:
        import json
        sets = row.get("sets")
        if isinstance(sets, str):
            try:
                sets = json.loads(sets)
            except Exception:
                sets = []
        return Match(
            match_id=row["id"],
            tournament_id=row.get("tournament_id"),
            pair_a_id=row.get("pair_a_id"),
            pair_b_id=row.get("pair_b_id"),
            date_time=row.get("date_time"),
            status=row.get("status", "SCHEDULED"),
            court_id=row.get("court_id"),
            round_id=row.get("round_id"),
            business_id=row.get("business_id"),
            created_by=row.get("created_by", ""),
            visibility=row.get("visibility", "PRIVATE"),
            sets=sets or [],
            current_set_index=row.get("current_set_index", 0),
            winner_pair_id=row.get("winner_pair_id"),
            winner_team=row.get("winner_team"),
            start_time_ms=row.get("start_time_ms"),
            elapsed_time_sec=row.get("elapsed_time_sec", 0),
            golden_point=bool(row.get("golden_point", 0)),
            sets_to_win=row.get("sets_to_win", 2),
            round_name=row.get("round_name"),
            deleted_at=row.get("deleted_at"),
        )
