from typing import Optional, List, Dict, Any

from sqlalchemy import text

from domain.repositories.court_repository import CourtRepository
from infrastructure.config.database import engine


class SqlCourtRepository(CourtRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM courts ORDER BY number"))
            return [dict(row) for row in result.mappings()]

    def get_by_id(self, court_id: str) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM courts WHERE id = :id"), {"id": court_id})
            row = result.mappings().first()
            if not row:
                return None
            return dict(row)

    def update(self, court_id: str, court_data: Dict[str, Any]) -> Dict[str, Any]:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM courts WHERE id = :id"), {"id": court_id})
            if not result.mappings().first():
                raise ValueError("Court not found")
            conn.execute(text("""
                UPDATE courts SET name = :name, location = :location, number = :number,
                    status = :status
                WHERE id = :id
            """), {
                "id": court_id, "name": court_data["name"], "location": court_data.get("location"),
                "number": court_data.get("number"), "status": court_data["status"],
            })
        return {**court_data, "id": court_id}
