"""SQLAlchemy match event repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.match_event import MatchEvent
from domain.repositories.match_event_repository import IMatchEventRepository


class SQLAlchemyMatchEventRepository(IMatchEventRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_match(self, match_id: str) -> List[MatchEvent]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT * FROM match_events WHERE match_id = :mid ORDER BY timestamp
            """), {"mid": match_id}).mappings().all()
            return [self._to_entity(dict(row)) for row in rows]

    def save(self, event: MatchEvent) -> MatchEvent:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO match_events (id, match_id, set_number, game_number, timestamp,
                    winning_pair_id, player_id, event_type, description, score_snapshot)
                VALUES (:id, :match_id, :set_number, :game_number, :timestamp,
                    :winning_pair_id, :player_id, :event_type, :description, :score_snapshot)
                ON DUPLICATE KEY UPDATE
                    event_type = VALUES(event_type), description = VALUES(description)
            """), {
                "id": event.id, "match_id": event.match_id,
                "set_number": event.set_number, "game_number": event.game_number,
                "timestamp": event.timestamp, "winning_pair_id": event.winning_pair_id,
                "player_id": event.player_id, "event_type": event.event_type,
                "description": event.description,
                "score_snapshot": str(event.score_snapshot) if event.score_snapshot else None,
            })
        return event

    def _to_entity(self, row: dict) -> MatchEvent:
        import json
        snapshot = row.get("score_snapshot")
        if isinstance(snapshot, str):
            try:
                snapshot = json.loads(snapshot)
            except Exception:
                snapshot = None
        return MatchEvent(
            event_id=row["id"],
            match_id=row["match_id"],
            event_type=row["event_type"],
            set_number=row["set_number"],
            timestamp=row["timestamp"],
            game_number=row.get("game_number"),
            winning_pair_id=row.get("winning_pair_id"),
            player_id=row.get("player_id"),
            description=row.get("description"),
            score_snapshot=snapshot,
        )
