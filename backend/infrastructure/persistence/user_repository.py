from typing import Optional, List, Dict, Any
from datetime import datetime

from sqlalchemy import text

from domain.repositories.user_repository import UserRepository
from infrastructure.config.database import engine
from infrastructure.config.security import decode_token
from infrastructure.mappers.response_builder import UserResponseBuilder


class SqlUserRepository(UserRepository):
    def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT u.*, ua.email as auth_email,
                       (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                FROM users u
                LEFT JOIN users_auth ua ON u.id = ua.user_id
                WHERE u.id = :id
            """), {"id": user_id})
            row = result.mappings().first()
            return dict(row) if row else None

    def get_all(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT u.*, ua.email as auth_email,
                       (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                FROM users u
                LEFT JOIN users_auth ua ON u.id = ua.user_id
                ORDER BY u.points DESC
            """))
            return [dict(row) for row in result.mappings()]

    def get_all_with_auth_and_role(self) -> List[Dict[str, Any]]:
        return self.get_all()

    def get_with_auth_and_role(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.get_by_id(user_id)

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT user_id FROM users_auth WHERE email = :email"), {"email": email})
            row = result.mappings().first()
            return dict(row) if row else None

    def register(self, email: str, password: str, name: Optional[str],
                 surname: Optional[str], username: Optional[str],
                 role: str, avatar: Optional[str] = None,
                 level: Optional[str] = None, position: Optional[str] = None,
                 dominant_hand: Optional[str] = None,
                 points: int = 0) -> Dict[str, Any]:
        import bcrypt
        with engine.begin() as conn:
            result = conn.execute(text("SELECT user_id FROM users_auth WHERE email = :email"), {"email": email})
            if result.mappings().first():
                raise ValueError("Email already registered")

            user_id = "usr_" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            conn.execute(text("""
                INSERT INTO users (id, name, surname, username, email, avatar, account_type, status, level, position, dominant_hand, points)
                VALUES (:id, :name, :surname, :username, :email, :avatar, 'USER', 'ACTIVE', :level, :position, :dominant_hand, :points)
            """), {
                "id": user_id, "name": name, "surname": surname,
                "username": username or email.split("@")[0], "email": email,
                "avatar": avatar, "level": level, "position": position,
                "dominant_hand": dominant_hand, "points": points,
            })

            conn.execute(text("""
                INSERT INTO users_auth (user_id, email, hashed_password)
                VALUES (:user_id, :email, :hashed_password)
                ON DUPLICATE KEY UPDATE
                    email = VALUES(email),
                    hashed_password = VALUES(hashed_password)
            """), {"user_id": user_id, "email": email, "hashed_password": hashed})

            role_row = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": role}).mappings().first()
            role_id = role_row["id"] if role_row else conn.execute(text("INSERT INTO roles (name) VALUES (:name)"), {"name": role}).lastrowid
            conn.execute(text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"), {"user_id": user_id, "role_id": role_id})

        return {"user_id": user_id, "role": role}

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        import bcrypt
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO users (id, name, surname, username, email, avatar, account_type, status, level, position, dominant_hand, points)
                VALUES (:id, :name, :surname, :username, :email, :avatar, 'USER', 'ACTIVE', :level, :position, :dominant_hand, :points)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name), surname = VALUES(surname), username = VALUES(username),
                    email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level),
                    position = VALUES(position), dominant_hand = VALUES(dominant_hand),
                    points = VALUES(points)
            """), {
                "id": user_data["id"], "name": user_data["name"],
                "surname": user_data.get("surname", ""), "username": user_data["username"],
                "email": user_data.get("email"), "avatar": user_data.get("avatar"),
                "level": user_data.get("level"), "position": user_data.get("position"),
                "dominant_hand": user_data.get("dominant_hand"), "points": user_data.get("points", 0),
            })

            if user_data.get("email"):
                hashed = bcrypt.hashpw((user_data.get("password") or "password").encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                conn.execute(text("""
                    INSERT INTO users_auth (user_id, email, hashed_password)
                    VALUES (:user_id, :email, :hashed_password)
                    ON DUPLICATE KEY UPDATE email = VALUES(email), hashed_password = VALUES(hashed_password)
                """), {"user_id": user_data["id"], "email": user_data["email"], "hashed_password": hashed})

            if user_data.get("role"):
                role_row = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": user_data["role"]}).mappings().first()
                role_id = role_row["id"] if role_row else conn.execute(text("INSERT INTO roles (name) VALUES (:name)"), {"name": user_data["role"]}).lastrowid
                conn.execute(text("""
                    INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)
                    ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
                """), {"user_id": user_data["id"], "role_id": role_id})

        return user_data

    def update(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
            if not result.mappings().first():
                raise ValueError("User not found")
            conn.execute(text("""
                UPDATE users SET name = :name, surname = :surname, username = :username,
                    email = :email, avatar = :avatar, level = :level,
                    position = :position, dominant_hand = :dominant_hand,
                    points = :points
                WHERE id = :id
            """), {
                "id": user_id, "name": user_data["name"], "surname": user_data.get("surname", ""),
                "username": user_data["username"], "email": user_data.get("email"),
                "avatar": user_data.get("avatar"), "level": user_data.get("level"),
                "position": user_data.get("position"), "dominant_hand": user_data.get("dominant_hand"),
                "points": user_data.get("points", 0),
            })
        return {**user_data, "id": user_id}

    def delete(self, user_id: str) -> None:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
            if not result.mappings().first():
                raise ValueError("User not found")
            conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})

    def get_role(self, user_id: str) -> Optional[str]:
        with engine.connect() as conn:
            result = conn.execute(text("""
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
            """), {"uid": user_id})
            row = result.mappings().first()
            return row["name"] if row else "PLAYER"

    def get_privacy_settings(self, user_id: str) -> Dict[str, str]:
        with engine.connect() as conn:
            try:
                row = conn.execute(text("""
                    SELECT profile_visibility, points_visibility, games_visibility, tournaments_visibility
                    FROM privacy_settings WHERE user_id = :uid
                """), {"uid": user_id}).mappings().first()
                if row:
                    return dict(row)
            except Exception:
                pass
        return {
            "profile_visibility": "PUBLIC",
            "points_visibility": "PUBLIC",
            "games_visibility": "PUBLIC",
            "tournaments_visibility": "PUBLIC",
        }

    def update_last_login(self, user_id: str) -> None:
        try:
            with engine.begin() as conn:
                conn.execute(text("UPDATE users_auth SET last_login = :now WHERE user_id = :uid"),
                             {"now": datetime.utcnow(), "uid": user_id})
        except Exception:
            pass

    def get_all_for_db_view(self) -> List[Dict[str, Any]]:
        return self.get_all()

    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        import bcrypt
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users_auth WHERE email = :email"), {"email": email})
            row = result.mappings().first()
            if not row:
                return None
            auth_user = dict(row)
            if not bcrypt.checkpw(password.encode("utf-8"), auth_user["hashed_password"].encode("utf-8")):
                return None
            user_id = auth_user.get("user_id") or auth_user.get("id")
            role = auth_user.get("role")
            if role is None:
                role = self.get_role(user_id)
            self.update_last_login(user_id)
            from infrastructure.config.security import create_access_token
            token = create_access_token(str(user_id), str(role))
            return {"access_token": token, "token_type": "bearer", "user_id": user_id, "role": role}

    def get_initial_user(self) -> Dict[str, Any]:
        from infrastructure.config.database import load_mock_data
        data = load_mock_data()
        return data["initial_user"]
