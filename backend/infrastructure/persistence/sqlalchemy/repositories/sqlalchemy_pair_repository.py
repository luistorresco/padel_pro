"""SQLAlchemy pair repository implementation."""

from typing import Optional, List, Dict
from sqlalchemy import text
from domain.entities.pair import Pair
from domain.repositories.pair_repository import IPairRepository


class SQLAlchemyPairRepository(IPairRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_id(self, pair_id: str) -> Optional[Pair]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM pairs WHERE id = :id"),
                {"id": pair_id}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def save(self, pair: Pair) -> Pair:
        with self.engine.begin() as conn:
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
                "id": pair.id, "name": pair.name,
                "player1_id": pair.player1_id, "player2_id": pair.player2_id,
                "created_by": pair.created_by, "status": pair.status,
                "tournaments_disputed": pair.tournaments_disputed,
                "titles_won": pair.titles_won,
            })
        return pair

    def delete(self, pair_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM pairs WHERE id = :id"), {"id": pair_id})

    def list_all(self) -> List[Pair]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("SELECT * FROM pairs ORDER BY created_at")).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def find_by_players(self, player1_id: str, player2_id: str) -> Optional[Pair]:
        with self.engine.connect() as conn:
            row = conn.execute(text("""
                SELECT * FROM pairs
                WHERE (player1_id = :p1 AND player2_id = :p2)
                   OR (player1_id = :p2 AND player2_id = :p1)
            """), {"p1": player1_id, "p2": player2_id}).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def find_with_players(self, pair_id: str) -> Optional[Dict]:
        with self.engine.connect() as conn:
            row = conn.execute(text("""
                SELECT p.*, u1.name as player1_name, u2.name as player2_name,
                       u1.avatar as player1_avatar, u2.avatar as player2_avatar,
                       u1.level as p1_level, u2.level as p2_level,
                       u1.points as p1_points, u2.points as p2_points
                FROM pairs p
                LEFT JOIN users u1 ON p.player1_id = u1.id
                LEFT JOIN users u2 ON p.player2_id = u2.id
                WHERE p.id = :id
            """), {"id": pair_id}).mappings().first()
            if not row:
                return None
            return dict(row)

    def _to_entity(self, row: dict) -> Pair:
        return Pair(
            pair_id=row["id"],
            name=row.get("name"),
            player1_id=row["player1_id"],
            player2_id=row["player2_id"],
            created_by=row["created_by"],
            status=row.get("status", "ACTIVE"),
            tournaments_disputed=row.get("tournaments_disputed", 0),
            titles_won=row.get("titles_won", 0),
            created_at=row.get("created_at"),
        )
