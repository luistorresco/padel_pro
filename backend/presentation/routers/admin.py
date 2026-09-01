"""Admin router."""

from fastapi import APIRouter, Depends

from presentation.deps_module import run_migrations_uc, require_admin

admin_router = APIRouter()


@admin_router.post("/migrate")
@admin_router.get("/migrate")
def admin_migrate(payload: dict = Depends(require_admin)):
    return run_migrations_uc.execute()
