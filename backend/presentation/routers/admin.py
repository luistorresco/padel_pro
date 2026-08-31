"""Admin router."""

from fastapi import APIRouter, Depends, Request, Body
from sqlalchemy import text

from infrastructure.database import engine
from presentation.deps_module import require_admin

admin_router = APIRouter()


@admin_router.post("/migrate")
@admin_router.get("/migrate")
def admin_migrate(request: Request, payload: dict = Depends(require_admin), body: dict | None = None):
    from infrastructure.migrations import run_migrations
    with engine.begin() as conn:
        run_migrations(conn)
    return {"status": "ok", "message": "Migration applied"}
