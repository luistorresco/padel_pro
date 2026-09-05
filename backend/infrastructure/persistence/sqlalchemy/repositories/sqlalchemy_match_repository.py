"""SQLAlchemy match repository implementation."""

from typing import Optional, List, Dict
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

    def update_court(self, match_id: str, court_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                UPDATE matches SET court_id = :court_id WHERE id = :id
            """), {"id": match_id, "court_id": court_id})

    def finish(self, match_id: str, winner_pair_id: str, winner_team: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                UPDATE matches SET status = 'FINISHED', winner_pair_id = :winner_id, winner_team = :winner_team
                WHERE id = :id
            """), {"id": match_id, "winner_id": winner_pair_id, "winner_team": winner_team})

    def update(self, match_id: str, data: Dict) -> None:
        if not data:
            return
        allowed_fields = {
            "tournament_id", "round_id", "business_id", "court_id", "created_by",
            "pair_a_id", "pair_b_id", "date_time", "status", "visibility", "sets",
            "current_set_index", "winner_pair_id", "winner_team", "start_time_ms",
            "elapsed_time_sec", "golden_point", "sets_to_win", "round_name", "deleted_at",
        }
        set_parts = []
        params = {"id": match_id}
        for key, value in data.items():
            if key in allowed_fields:
                set_parts.append(f"{key} = :{key}")
                params[key] = value
        if not set_parts:
            return
        sql = f"UPDATE matches SET {', '.join(set_parts)} WHERE id = :id"
        with self.engine.begin() as conn:
            conn.execute(text(sql), params)

    def find_all_detailed(self) -> List[Dict]:
        with self.engine.connect() as conn:
            try:
                rows = conn.execute(text("""
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
                    WHERE m.deleted_at IS NULL
                    ORDER BY m.date_time
                """)).mappings().all()
            except Exception:
                rows = conn.execute(text("""
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
                    WHERE m.deleted_at IS NULL
                    ORDER BY m.date_time
                """)).mappings().all()
            return [dict(r) for r in rows]

    def find_by_id_detailed(self, match_id: str) -> Optional[Dict]:
        with self.engine.connect() as conn:
            row = conn.execute(text("""
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
            """), {"id": match_id}).mappings().first()
            if not row:
                return None
            return dict(row)

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
