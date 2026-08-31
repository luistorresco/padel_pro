"""SQLAlchemy role repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.role import Role
from domain.repositories.role_repository import IRoleRepository


class SQLAlchemyRoleRepository(IRoleRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_id(self, role_id: int) -> Optional[Role]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM roles WHERE id = :id"),
                {"id": role_id}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def find_by_name(self, name: str) -> Optional[Role]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM roles WHERE name = :name"),
                {"name": name}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def save(self, role: Role) -> Role:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO roles (id, name, description) VALUES (:id, :name, :description)
                ON DUPLICATE KEY UPDATE name = VALUES(name), description = VALUES(description)
            """), {"id": role.id, "name": role.name, "description": role.description})
        return role

    def list_all(self) -> List[Role]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("SELECT * FROM roles")).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def _to_entity(self, row: dict) -> Role:
        return Role(
            role_id=row["id"],
            name=row["name"],
            description=row.get("description"),
        )
