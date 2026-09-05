"""Thin FastAPI app factory - hexagonal entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy import text

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
        allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(","),
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
                        try:
                            result = conn.execute(__import__('sqlalchemy').text("SELECT COUNT(*) as cnt FROM users"))
                            cnt = result.mappings().first()["cnt"]
                            if cnt == 0:
                                from seed_full import main as seed_main
                                seed_main()
                                print("[db] Database seeded on startup (admin missing).")
                            else:
                                admin_id = "usr_admin_super"
                                admin_email = "admin@padelpro.app"
                                admin_name = "Admin User"
                                from domain.services.auth_service import AuthService
                                hashed = AuthService(secret_key=os.environ.get("JWT_SECRET_KEY", "padel-pro-secret-key-change-in-production")).hash_password("admin123")
                                conn.execute(text("""
                                    INSERT INTO users (id, name, surname, username, email, account_type, status, points)
                                    VALUES (:id, :name, :surname, :username, :email, 'USER', 'ACTIVE', 0)
                                    ON DUPLICATE KEY UPDATE name = VALUES(name)
                                """), {
                                    "id": admin_id,
                                    "name": admin_name,
                                    "surname": "System",
                                    "username": "admin",
                                    "email": admin_email,
                                })
                                conn.execute(text("""
                                    INSERT INTO users_auth (user_id, email, hashed_password)
                                    VALUES (:user_id, :email, :hashed_password)
                                    ON DUPLICATE KEY UPDATE email = VALUES(email), hashed_password = VALUES(hashed_password)
                                """), {"user_id": admin_id, "email": admin_email, "hashed_password": hashed})
                                role_id = conn.execute(text("SELECT id FROM roles WHERE name = 'SUPER_ADMIN'")).scalar()
                                if role_id:
                                    conn.execute(text("""
                                        INSERT INTO user_roles (user_id, role_id)
                                        VALUES (:user_id, :role_id)
                                        ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
                                    """), {"user_id": admin_id, "role_id": role_id})
                                print(f"[db] Created admin user: {admin_email} / admin123")
                        except Exception as admin_create_err:
                            print(f"[db] Admin creation warning: {admin_create_err}")
                except Exception as admin_err:
                    print(f"[db] Admin check warning: {admin_err}")
            print("[db] Migrations applied on startup.")
        except Exception as e:
            print(f"[db] Startup migration warning: {e}")

    return app


app = create_app()
