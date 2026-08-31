"""Courts router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from sqlalchemy import text

from infrastructure.database import engine
from presentation.deps_module import require_admin

courts_router = APIRouter()


@courts_router.get("")
def get_courts():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courts ORDER BY created_at"))
        return [dict(row) for row in result.mappings()]


@courts_router.get("/{court_id}")
def get_court(court_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courts WHERE id = :id"), {"id": court_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Court not found")
        return dict(row)


@courts_router.post("")
def create_court(court: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO courts (id, business_id, name, location, number, status)
            VALUES (:id, :business_id, :name, :location, :number, :status)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), location = VALUES(location),
                number = VALUES(number), status = VALUES(status)
        """), {
            "id": court["id"],
            "business_id": court.get("business_id"),
            "name": court["name"],
            "location": court.get("location"),
            "number": court.get("number"),
            "status": court.get("status", "AVAILABLE"),
        })
    return court


@courts_router.put("/{court_id}")
def update_court(court_id: str, court: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE courts SET
                name = :name, location = :location, number = :number, status = :status
            WHERE id = :id
        """), {
            "id": court_id,
            "name": court.get("name"),
            "location": court.get("location"),
            "number": court.get("number"),
            "status": court.get("status", "AVAILABLE"),
        })
    return {"id": court_id, **court}


@courts_router.delete("/{court_id}")
def delete_court(court_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM courts WHERE id = :id"), {"id": court_id})
    return {"message": "Court deleted"}
