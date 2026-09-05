"""SQLAlchemy user repository implementation."""

from typing import Optional, List, Dict
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

    def find_auth_by_email(self, email: str) -> Optional[Dict]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM users_auth WHERE email = :email"),
                {"email": email}
            ).mappings().first()
            if not row:
                return None
            return dict(row)

    def find_role_by_user(self, user_id: str) -> Optional[str]:
        with self.engine.connect() as conn:
            row = conn.execute(text("""
                SELECT r.name FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id
                WHERE ur.user_id = :uid
                ORDER BY CASE r.name
                    WHEN 'SUPER_ADMIN' THEN 1
                    WHEN 'BUSINESS_ADMIN' THEN 2
                    WHEN 'BUSINESS_MANAGER' THEN 3
                    WHEN 'ADMIN' THEN 4
                    WHEN 'USER' THEN 5
                    ELSE 6
                END
                LIMIT 1
            """), {"uid": user_id}).mappings().first()
            if row:
                return row["name"]
            return None

    def update_last_login(self, user_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text("UPDATE users_auth SET last_login = :now WHERE user_id = :uid"),
                {"now": __import__('datetime').datetime.utcnow(), "uid": user_id}
            )

    def find_privacy(self, user_id: str) -> Dict:
        with self.engine.connect() as conn:
            try:
                row = conn.execute(text("""
                    SELECT profile_visibility, points_visibility, games_visibility, tournaments_visibility
                    FROM privacy_settings WHERE user_id = :uid
                """), {"uid": user_id}).mappings().first()
                if row:
                    return dict(row)
            except Exception:
                pass
            return {}

    def create_auth(self, user_id: str, email: str, hashed_password: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO users_auth (user_id, email, hashed_password)
                VALUES (:user_id, :email, :hashed_password)
                ON DUPLICATE KEY UPDATE email = VALUES(email), hashed_password = VALUES(hashed_password)
            """), {"user_id": user_id, "email": email, "hashed_password": hashed_password})

    def assign_role(self, user_id: str, role_name: str) -> None:
        with self.engine.begin() as conn:
            role_id = conn.execute(
                text("SELECT id FROM roles WHERE name = :name"),
                {"name": role_name}
            ).scalar()
            if not role_id:
                role_id = conn.execute(
                    text("INSERT INTO roles (name) VALUES (:name)"),
                    {"name": role_name}
                ).lastrowid
            conn.execute(text("""
                INSERT INTO user_roles (user_id, role_id)
                VALUES (:user_id, :role_id)
                ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
            """), {"user_id": user_id, "role_id": role_id})

    def hard_delete(self, user_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM user_roles WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM profiles WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM privacy_settings WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM business_users WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM user_points WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM notifications WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM audit_logs WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM tournament_players WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM match_players WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("UPDATE pairs SET player1_id = NULL WHERE player1_id = :id"), {"id": user_id})
            conn.execute(text("UPDATE pairs SET player2_id = NULL WHERE player2_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM users_auth WHERE user_id = :id"), {"id": user_id})
            conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})

    def find_with_role(self, user_id: str) -> Optional[Dict]:
        with self.engine.connect() as conn:
            row = conn.execute(text("""
                SELECT u.*, ua.email as auth_email,
                       (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                FROM users u
                LEFT JOIN users_auth ua ON u.id = ua.user_id
                WHERE u.id = :id
            """), {"id": user_id}).mappings().first()
            if not row:
                return None
            return dict(row)

    def update_privacy(self, user_id: str, privacy_data: Dict) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO privacy_settings (user_id, profile_visibility, points_visibility, games_visibility, tournaments_visibility)
                VALUES (:user_id, :profile_visibility, :points_visibility, :games_visibility, :tournaments_visibility)
                ON DUPLICATE KEY UPDATE
                    profile_visibility = VALUES(profile_visibility),
                    points_visibility = VALUES(points_visibility),
                    games_visibility = VALUES(games_visibility),
                    tournaments_visibility = VALUES(tournaments_visibility)
            """), {
                "user_id": user_id,
                "profile_visibility": privacy_data.get("profile_visibility", "PUBLIC"),
                "points_visibility": privacy_data.get("points_visibility", "PUBLIC"),
                "games_visibility": privacy_data.get("games_visibility", "PUBLIC"),
                "tournaments_visibility": privacy_data.get("tournaments_visibility", "PUBLIC"),
            })

    def save(self, user: User) -> User:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO users (id, name, surname, username, email, avatar, account_type, status,
                    level, position, dominant_hand, points, invited_by, invitation_code, converted_at, deleted_at,
                    matches_played, matches_won, matches_lost, sets_won, sets_lost, games_won, games_lost)
                VALUES (:id, :name, :surname, :username, :email, :avatar, :account_type, :status,
                    :level, :position, :dominant_hand, :points, :invited_by, :invitation_code, :converted_at, :deleted_at,
                    :matches_played, :matches_won, :matches_lost, :sets_won, :sets_lost, :games_won, :games_lost)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name), surname = VALUES(surname), username = VALUES(username),
                    email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level),
                    position = VALUES(position), dominant_hand = VALUES(dominant_hand),
                    points = VALUES(points), deleted_at = VALUES(deleted_at),
                    matches_played = VALUES(matches_played), matches_won = VALUES(matches_won),
                    matches_lost = VALUES(matches_lost), sets_won = VALUES(sets_won),
                    sets_lost = VALUES(sets_lost), games_won = VALUES(games_won),
                    games_lost = VALUES(games_lost)
            """), {
                "id": user.id, "name": user.name, "surname": user.surname,
                "username": user.username, "email": user.email, "avatar": user.avatar,
                "account_type": user.account_type, "status": user.status,
                "level": user.level, "position": user.position,
                "dominant_hand": user.dominant_hand, "points": user.points,
                "invited_by": user.invited_by, "invitation_code": user.invitation_code,
                "converted_at": user.converted_at, "deleted_at": user.deleted_at,
                "matches_played": getattr(user, 'matches_played', 0),
                "matches_won": getattr(user, 'matches_won', 0),
                "matches_lost": getattr(user, 'matches_lost', 0),
                "sets_won": getattr(user, 'sets_won', 0),
                "sets_lost": getattr(user, 'sets_lost', 0),
                "games_won": getattr(user, 'games_won', 0),
                "games_lost": getattr(user, 'games_lost', 0),
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

    def list_by_inviter(self, inviter_id: str, limit: int = 100) -> List[User]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT * FROM users WHERE deleted_at IS NULL AND invited_by = :inviter_id
                ORDER BY created_at DESC LIMIT :limit
            """), {"inviter_id": inviter_id, "limit": limit}).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def find_guest_by_invitation_code(self, invitation_code: str) -> Optional[User]:
        with self.engine.connect() as conn:
            row = conn.execute(text("""
                SELECT * FROM users WHERE invitation_code = :code AND account_type = 'GUEST' AND deleted_at IS NULL
            """), {"code": invitation_code}).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

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
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            matches_played=row.get("matches_played", 0),
            matches_won=row.get("matches_won", 0),
            matches_lost=row.get("matches_lost", 0),
            sets_won=row.get("sets_won", 0),
            sets_lost=row.get("sets_lost", 0),
            games_won=row.get("games_won", 0),
            games_lost=row.get("games_lost", 0),
        )
