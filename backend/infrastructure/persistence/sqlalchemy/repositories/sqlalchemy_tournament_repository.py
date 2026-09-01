"""SQLAlchemy tournament repository implementation."""

from typing import Optional, List, Dict
from sqlalchemy import text
from domain.entities.tournament import Tournament
from domain.repositories.tournament_repository import ITournamentRepository


class SQLAlchemyTournamentRepository(ITournamentRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_id(self, tournament_id: str) -> Optional[Tournament]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM tournaments WHERE id = :id"),
                {"id": tournament_id}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def save(self, tournament: Tournament) -> Tournament:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO tournaments (id, business_id, created_by, name, logo, description,
                    category, level, location, start_date, end_date, status, format, max_pairs,
                    visibility, rules, deleted_at)
                VALUES (:id, :business_id, :created_by, :name, :logo, :description,
                    :category, :level, :location, :start_date, :end_date, :status, :format, :max_pairs,
                    :visibility, :rules, :deleted_at)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name), description = VALUES(description),
                    category = VALUES(category), level = VALUES(level),
                    location = VALUES(location), start_date = VALUES(start_date),
                    end_date = VALUES(end_date), status = VALUES(status),
                    format = VALUES(format), max_pairs = VALUES(max_pairs),
                    visibility = VALUES(visibility), rules = VALUES(rules),
                    deleted_at = VALUES(deleted_at)
            """), {
                "id": tournament.id, "business_id": tournament.business_id,
                "created_by": tournament.created_by, "name": tournament.name,
                "logo": tournament.logo, "description": tournament.description,
                "category": tournament.category, "level": tournament.level,
                "location": tournament.location, "start_date": tournament.start_date,
                "end_date": tournament.end_date, "status": tournament.status,
                "format": tournament.format, "max_pairs": tournament.max_pairs,
                "visibility": tournament.visibility,
                "rules": str(tournament.rules) if tournament.rules else None,
                "deleted_at": tournament.deleted_at,
            })
        return tournament

    def delete(self, tournament_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text("UPDATE tournaments SET deleted_at = NOW() WHERE id = :id"),
                {"id": tournament_id}
            )

    def list_all(self) -> List[Tournament]:
        with self.engine.connect() as conn:
            rows = conn.execute(
                text("SELECT * FROM tournaments WHERE deleted_at IS NULL ORDER BY start_date")
            ).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def find_full(self, tournament_id: str) -> Optional[dict]:
        with self.engine.connect() as conn:
            tournament = self.find_by_id(tournament_id)
            if not tournament:
                return None

            categories = conn.execute(text("""
                SELECT * FROM tournament_categories WHERE tournament_id = :tid
            """), {"tid": tournament_id}).mappings().all()

            rounds = conn.execute(text("""
                SELECT * FROM tournament_rounds WHERE tournament_id = :tid
            """), {"tid": tournament_id}).mappings().all()

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
                SELECT * FROM matches WHERE tournament_id = :tid AND deleted_at IS NULL
                ORDER BY date_time
            """), {"tid": tournament_id}).mappings().all()

            return {
                "tournament": tournament.__dict__,
                "categories": [dict(c) for c in categories],
                "rounds": [dict(r) for r in rounds],
                "pairs": [dict(p) for p in pairs],
                "players": [dict(p) for p in players],
                "matches": [dict(m) for m in matches],
            }

    def register_pair(self, tournament_id: str, pair_id: str, status: str = "REGISTERED") -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO tournament_pairs (tournament_id, pair_id, status)
                VALUES (:tid, :pid, :status)
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """), {"tid": tournament_id, "pid": pair_id, "status": status})

    def register_player(self, tournament_id: str, user_id: str, status: str = "REGISTERED") -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO tournament_players (tournament_id, user_id, status)
                VALUES (:tid, :uid, :status)
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """), {"tid": tournament_id, "uid": user_id, "status": status})

    def _to_entity(self, row: dict) -> Tournament:
        import json
        rules = row.get("rules")
        if isinstance(rules, str):
            try:
                rules = json.loads(rules)
            except Exception:
                rules = {}
        return Tournament(
            tournament_id=row["id"],
            name=row["name"],
            created_by=row["created_by"],
            start_date=row["start_date"],
            status=row.get("status", "DRAFT"),
            business_id=row.get("business_id"),
            logo=row.get("logo"),
            description=row.get("description"),
            category=row.get("category"),
            level=row.get("level"),
            location=row.get("location"),
            end_date=row.get("end_date"),
            format=row.get("format"),
            max_pairs=row.get("max_pairs"),
            visibility=row.get("visibility", "PRIVATE"),
            rules=rules or {},
            deleted_at=row.get("deleted_at"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )
