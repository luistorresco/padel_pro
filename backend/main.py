"""Thin FastAPI app factory - hexagonal entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from infrastructure.database import engine
from presentation.routers import (
    auth_router,
    users_router,
    pairs_router,
    tournaments_router,
    matches_router,
    courts_router,
    audit_logs_router,
    notifications_router,
    stats_router,
    admin_router,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Padel Pro API",
        description="API REST para la gestión de torneos de padel",
        version="2.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(users_router, prefix="/api/users", tags=["users"])
    app.include_router(pairs_router, prefix="/api/pairs", tags=["pairs"])
    app.include_router(tournaments_router, prefix="/api/tournaments", tags=["tournaments"])
    app.include_router(matches_router, prefix="/api/matches", tags=["matches"])
    app.include_router(courts_router, prefix="/api/courts", tags=["courts"])
    app.include_router(audit_logs_router, prefix="/api/audit-logs", tags=["audit-logs"])
    app.include_router(notifications_router, prefix="/api/notifications", tags=["notifications"])
    app.include_router(stats_router, prefix="/api/stats", tags=["stats"])
    app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": "padel-pro-backend", "version": "2.0.0"}

    @app.on_event("startup")
    def on_startup():
        try:
            from infrastructure.database import engine, create_schema, seed_roles
            with engine.begin() as conn:
                create_schema(conn)
                seed_roles(conn)
                from infrastructure.migrations import run_migrations
                run_migrations(conn)
                try:
                    result = conn.execute(__import__('sqlalchemy').text("SELECT COUNT(*) as cnt FROM users"))
                    cnt = result.mappings().first()["cnt"]
                    if cnt == 0:
                        from seed_full import main as seed_main
                        seed_main()
                        print("[db] Database seeded on startup.")
                    else:
                        print("[db] Database already contains data.")
                except Exception as seed_err:
                    print(f"[db] Seed check warning: {seed_err}")

                try:
                    admin_check = conn.execute(__import__('sqlalchemy').text("""
                        SELECT ua.user_id FROM users_auth ua
                        JOIN user_roles ur ON ua.user_id = ur.user_id
                        JOIN roles r ON ur.role_id = r.id
                        WHERE r.name = 'SUPER_ADMIN'
                        LIMIT 1
                    """)).mappings().first()
                    if not admin_check:
                        from seed_full import main as seed_main
                        seed_main()
                        print("[db] Ensured admin user exists on startup.")
                except Exception as admin_err:
                    print(f"[db] Admin check warning: {admin_err}")
            print("[db] Migrations applied on startup.")
        except Exception as e:
            print(f"[db] Startup migration warning: {e}")

    return app


app = create_app()
