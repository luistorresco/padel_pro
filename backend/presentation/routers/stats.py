"""Stats router."""

from fastapi import APIRouter
from sqlalchemy import text

from infrastructure.database import engine

stats_router = APIRouter()


@stats_router.get("")
def get_stats():
    with engine.connect() as conn:
        total_players = conn.execute(text("SELECT COUNT(*) FROM users WHERE deleted_at IS NULL")).scalar()
        total_matches = conn.execute(text("SELECT COUNT(*) FROM matches WHERE deleted_at IS NULL")).scalar()
        total_pairs = conn.execute(text("SELECT COUNT(*) FROM pairs")).scalar()
        total_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments WHERE deleted_at IS NULL")).scalar()
        total_courts = conn.execute(text("SELECT COUNT(*) FROM courts")).scalar()
        total_notifications = conn.execute(text("SELECT COUNT(*) FROM notifications WHERE read_status = 0")).scalar()
        total_audit_logs = conn.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar()

        live_matches = conn.execute(text("""
            SELECT COUNT(*) FROM matches WHERE status = 'IN_PROGRESS' AND deleted_at IS NULL
        """)).scalar()
        upcoming_matches = conn.execute(text("""
            SELECT COUNT(*) FROM matches WHERE status = 'SCHEDULED' AND deleted_at IS NULL
        """)).scalar()
        finished_matches = conn.execute(text="""
            SELECT COUNT(*) FROM matches WHERE status = 'FINISHED' AND deleted_at IS NULL
        """).scalar()
        open_tournaments = conn.execute(text("""
            SELECT COUNT(*) FROM tournaments WHERE status = 'OPEN' AND deleted_at IS NULL
        """)).scalar()
        draft_tournaments = conn.execute(text("""
            SELECT COUNT(*) FROM tournaments WHERE status = 'DRAFT' AND deleted_at IS NULL
        """)).scalar()

        return {
            "total_players": total_players,
            "total_matches": total_matches,
            "total_pairs": total_pairs,
            "total_tournaments": total_tournaments,
            "total_courts": total_courts,
            "total_notifications": total_notifications,
            "total_audit_logs": total_audit_logs,
            "live_matches": live_matches,
            "upcoming_matches": upcoming_matches,
            "finished_matches": finished_matches,
            "open_tournaments": open_tournaments,
            "draft_tournaments": draft_tournaments,
        }
