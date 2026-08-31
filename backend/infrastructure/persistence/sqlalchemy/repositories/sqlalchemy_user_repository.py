"""SQLAlchemy user repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.user import User
from domain.repositories.user_repository import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_id(self, user_id: str) -> Optional[User]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {"id": user_id}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def find_by_email(self, email: str) -> Optional[User]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": email}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def find_by_username(self, username: str) -> Optional[User]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def save(self, user: User) -> User:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO users (id, name, surname, username, email, avatar, account_type, status,
                    level, position, dominant_hand, points, invited_by, invitation_code, converted_at, deleted_at)
                VALUES (:id, :name, :surname, :username, :email, :avatar, :account_type, :status,
                    :level, :position, :dominant_hand, :points, :invited_by, :invitation_code, :converted_at, :deleted_at)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name), surname = VALUES(surname), username = VALUES(username),
                    email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level),
                    position = VALUES(position), dominant_hand = VALUES(dominant_hand),
                    points = VALUES(points), deleted_at = VALUES(deleted_at)
            """), {
                "id": user.id, "name": user.name, "surname": user.surname,
                "username": user.username, "email": user.email, "avatar": user.avatar,
                "account_type": user.account_type, "status": user.status,
                "level": user.level, "position": user.position,
                "dominant_hand": user.dominant_hand, "points": user.points,
                "invited_by": user.invited_by, "invitation_code": user.invitation_code,
                "converted_at": user.converted_at, "deleted_at": user.deleted_at,
            })
        return user

    def delete(self, user_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("UPDATE users SET deleted_at = NOW() WHERE id = :id"), {"id": user_id})

    def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT * FROM users WHERE deleted_at IS NULL
                ORDER BY points DESC LIMIT :limit OFFSET :skip
            """), {"limit": limit, "skip": skip}).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def _to_entity(self, row: dict) -> User:
        return User(
            user_id=row["id"],
            name=row["name"],
            surname=row.get("surname", ""),
            username=row["username"],
            email=row.get("email", ""),
            avatar=row.get("avatar"),
            account_type=row.get("account_type", "GUEST"),
            status=row.get("status", "ACTIVE"),
            level=row.get("level"),
            position=row.get("position"),
            dominant_hand=row.get("dominant_hand"),
            points=row.get("points", 0),
            invited_by=row.get("invited_by"),
            invitation_code=row.get("invitation_code"),
            converted_at=row.get("converted_at"),
            deleted_at=row.get("deleted_at"),
        )
