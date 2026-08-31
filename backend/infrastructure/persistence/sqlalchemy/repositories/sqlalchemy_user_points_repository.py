"""SQLAlchemy user points repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.user_points import UserPoints
from domain.repositories.user_points_repository import IUserPointsRepository


class SQLAlchemyUserPointsRepository(IUserPointsRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_user(self, user_id: str) -> List[UserPoints]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT * FROM user_points WHERE user_id = :uid
            """), {"uid": user_id}).mappings().all()
            return [self._to_entity(dict(row)) for row in rows]

    def save(self, user_points: UserPoints) -> UserPoints:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO user_points (user_id, match_id, tournament_id, points, reason)
                VALUES (:user_id, :match_id, :tournament_id, :points, :reason)
                ON DUPLICATE KEY UPDATE
                    points = VALUES(points), reason = VALUES(reason)
            """), {
                "user_id": user_points.user_id,
                "match_id": user_points.match_id,
                "tournament_id": user_points.tournament_id,
                "points": user_points.points,
                "reason": user_points.reason,
            })
        return user_points

    def _to_entity(self, row: dict) -> UserPoints:
        return UserPoints(
            user_id=row["user_id"],
            match_id=row.get("match_id"),
            tournament_id=row.get("tournament_id"),
            points=row["points"],
            reason=row.get("reason"),
        )
