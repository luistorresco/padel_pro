"""SQLAlchemy court repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.court import Court
from domain.repositories.court_repository import ICourtRepository


class SQLAlchemyCourtRepository(ICourtRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_id(self, court_id: str) -> Optional[Court]:
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM courts WHERE id = :id"),
                {"id": court_id}
            ).mappings().first()
            if not row:
                return None
            return self._to_entity(dict(row))

    def save(self, court: Court) -> Court:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO courts (id, business_id, name, location, number, status)
                VALUES (:id, :business_id, :name, :location, :number, :status)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name), location = VALUES(location),
                    number = VALUES(number), status = VALUES(status)
            """), {
                "id": court.id, "business_id": court.business_id,
                "name": court.name, "location": court.location,
                "number": court.number, "status": court.status,
            })
        return court

    def delete(self, court_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM courts WHERE id = :id"), {"id": court_id})

    def list_all(self) -> List[Court]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("SELECT * FROM courts ORDER BY created_at")).mappings()
            return [self._to_entity(dict(row)) for row in rows]

    def _to_entity(self, row: dict) -> Court:
        return Court(
            court_id=row["id"],
            name=row["name"],
            business_id=row["business_id"],
            status=row.get("status", "AVAILABLE"),
            location=row.get("location"),
            number=row.get("number"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )
