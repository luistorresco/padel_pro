from typing import Optional, List, Tuple, Dict, Any

from sqlalchemy import text

from domain.repositories.pair_repository import PairRepository
from infrastructure.config.database import engine
from infrastructure.mappers.response_builder import PairResponseBuilder


class SqlPairRepository(PairRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT p.id, p.name, p.status, p.created_at, p.updated_at,
                       p.tournaments_disputed, p.titles_won,
                       p.player1_id, p.player2_id,
                       u1.name AS player1_name, u1.surname AS player1_surname,
                       u1.avatar AS player1_avatar, u1.username AS player1_username,
                       u2.name AS player2_name, u2.surname AS player2_surname,
                       u2.avatar AS player2_avatar, u2.username AS player2_username
                FROM pairs p
                JOIN users u1 ON p.player1_id = u1.id
                JOIN users u2 ON p.player2_id = u2.id
                ORDER BY p.created_at
            """))
            pairs = []
            for row in result.mappings():
                r = dict(row)
                pairs.append(PairResponseBuilder.build_simple(r))
            return pairs

    def get_by_id(self, pair_id: str) -> Optional[Dict[str, Any]]:
        pair = self.get_pair_with_users(pair_id)
        if not pair:
            return None
        return PairResponseBuilder.build_enriched(pair)

    def create(self, pair_data: Dict[str, Any]) -> Dict[str, Any]:
        player1_id = pair_data.get("player1Id") or pair_data.get("player1_id")
        player2_id = pair_data.get("player2Id") or pair_data.get("player2_id")

        valid, msg = self.validate_players_exist(player1_id, player2_id)
        if not valid:
            raise ValueError(msg)

        with engine.begin() as conn:
            pair_id = pair_data.get("id") or f"{player1_id}_{player2_id}"
            conn.execute(text("""
                INSERT INTO pairs (id, name, player1_id, player2_id, created_by, status, tournaments_disputed, titles_won)
                VALUES (:id, :name, :player1_id, :player2_id, :created_by, :status, :tournaments_disputed, :titles_won)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id),
                    created_by = VALUES(created_by), status = VALUES(status),
                    tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won)
            """), {
                "id": pair_id,
                "name": pair_data.get("name"),
                "player1_id": player1_id,
                "player2_id": player2_id,
                "created_by": pair_data.get("createdBy") or pair_data.get("created_by") or player1_id,
                "status": pair_data.get("status", "ACTIVE"),
                "tournaments_disputed": pair_data.get("tournamentsDisputed") or pair_data.get("tournaments_disputed") or 0,
                "titles_won": pair_data.get("titlesWon") or pair_data.get("titles_won") or 0,
            })

            enriched = self.get_pair_with_users(pair_id)
        if enriched:
            return PairResponseBuilder.build_enriched(enriched)
        return {"id": pair_id, **pair_data}

    def delete(self, pair_id: str) -> None:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM pairs WHERE id = :id"), {"id": pair_id})
            if not result.mappings().first():
                raise ValueError("Pair not found")
            conn.execute(text("DELETE FROM pairs WHERE id = :id"), {"id": pair_id})

    def validate_players_exist(self, player1_id: str, player2_id: str) -> Tuple[bool, str]:
        with engine.connect() as conn:
            r = conn.execute(text("SELECT COUNT(*) as cnt FROM users WHERE id = :id"), {"id": player1_id}).mappings().first()
            if not r or r["cnt"] == 0:
                return False, f"Player1 '{player1_id}' does not exist in users"
            r = conn.execute(text("SELECT COUNT(*) as cnt FROM users WHERE id = :id"), {"id": player2_id}).mappings().first()
            if not r or r["cnt"] == 0:
                return False, f"Player2 '{player2_id}' does not exist in users"
            if player1_id == player2_id:
                return False, "Pair must have two different players"
        return True, ""

    def get_pair_with_users(self, pair_id: str) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT p.*, u1.name as p1_name, u1.surname as p1_surname, u1.avatar as p1_avatar,
                       u1.username as p1_username, u1.level as p1_level, u1.points as p1_points,
                       u2.name as p2_name, u2.surname as p2_surname, u2.avatar as p2_avatar,
                       u2.username as p2_username, u2.level as p2_level, u2.points as p2_points
                FROM pairs p
                JOIN users u1 ON p.player1_id = u1.id
                JOIN users u2 ON p.player2_id = u2.id
                WHERE p.id = :id
            """), {"id": pair_id}).mappings().first()
            return dict(row) if row else None

    def get_all_pairs_with_users(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT p.id, p.name, p.status, p.tournaments_disputed, p.titles_won,
                       p.player1_id, p.player2_id,
                       u1.name as p1_name, u1.surname as p1_surname, u1.avatar as p1_avatar,
                       u1.username as p1_username,
                       u2.name as p2_name, u2.surname as p2_surname, u2.avatar as p2_avatar,
                       u2.username as p2_username
                FROM pairs p
                JOIN users u1 ON p.player1_id = u1.id
                JOIN users u2 ON p.player2_id = u2.id
                ORDER BY p.created_at
            """)).mappings().all()
            return [dict(r) for r in rows]
