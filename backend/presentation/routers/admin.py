"""Admin router."""

from fastapi import APIRouter, Depends
from sqlalchemy import text

from infrastructure.database import engine
from presentation.deps_module import require_admin

admin_router = APIRouter()


@admin_router.post("/migrate")
def admin_migrate(payload: dict = Depends(require_admin)):
    from infrastructure.migrations import run_migrations
    with engine.begin() as conn:
        run_migrations(conn)
    return {"status": "ok", "message": "Migration applied"}
