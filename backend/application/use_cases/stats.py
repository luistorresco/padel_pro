"""Stats use cases."""

from sqlalchemy import text


class GetStatsUseCase:
    def __init__(self, engine):
        self.engine = engine

    def execute(self):
        with self.engine.connect() as conn:
            total_players = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
            total_matches = conn.execute(text("SELECT COUNT(*) FROM matches")).scalar()
            total_pairs = conn.execute(text("SELECT COUNT(*) FROM pairs")).scalar()
            total_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments")).scalar()
            total_courts = conn.execute(text("SELECT COUNT(*) FROM courts")).scalar()
            total_notifications = conn.execute(text("SELECT COUNT(*) FROM notifications WHERE read_status = 0")).scalar()
            total_audit_logs = conn.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar()

            try:
                live_matches = conn.execute(text("""
                    SELECT COUNT(*) FROM matches WHERE status = 'IN_PROGRESS' AND deleted_at IS NULL
                """)).scalar()
            except Exception:
                live_matches = conn.execute(text("""
                    SELECT COUNT(*) FROM matches WHERE status = 'IN_PROGRESS'
                """)).scalar()

            try:
                upcoming_matches = conn.execute(text("""
                    SELECT COUNT(*) FROM matches WHERE status = 'SCHEDULED' AND deleted_at IS NULL
                """)).scalar()
            except Exception:
                upcoming_matches = conn.execute(text("""
                    SELECT COUNT(*) FROM matches WHERE status = 'SCHEDULED'
                """)).scalar()

            try:
                finished_matches = conn.execute(text("""
                    SELECT COUNT(*) FROM matches WHERE status = 'FINISHED' AND deleted_at IS NULL
                """)).scalar()
            except Exception:
                finished_matches = conn.execute(text("""
                    SELECT COUNT(*) FROM matches WHERE status = 'FINISHED'
                """)).scalar()

            try:
                open_tournaments = conn.execute(text("""
                    SELECT COUNT(*) FROM tournaments WHERE status = 'OPEN' AND deleted_at IS NULL
                """)).scalar()
            except Exception:
                open_tournaments = conn.execute(text("""
                    SELECT COUNT(*) FROM tournaments WHERE status = 'OPEN'
                """)).scalar()

            try:
                draft_tournaments = conn.execute(text("""
                    SELECT COUNT(*) FROM tournaments WHERE status = 'DRAFT' AND deleted_at IS NULL
                """)).scalar()
            except Exception:
                draft_tournaments = conn.execute(text("""
                    SELECT COUNT(*) FROM tournaments WHERE status = 'DRAFT'
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
