"""Run database migrations."""

from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


def run_migrations(conn):
    """Add missing columns to existing tables."""
    try:
        cols = [
            r["COLUMN_NAME"]
            for r in conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users_auth'
            """)).mappings()
        ]
        if "id" in cols and "user_id" not in cols:
            conn.execute(text("""
                ALTER TABLE users_auth CHANGE COLUMN id user_id VARCHAR(255) NOT NULL
            """))
        if "role" in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth DROP COLUMN role"))
            except Exception as e:
                logger.warning(f"Migration warning (users_auth role): {e}")
        if "last_login" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN last_login DATETIME NULL"))
            except Exception as e:
                logger.warning(f"Migration warning (users_auth last_login): {e}")
        if "email_verified_at" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN email_verified_at DATETIME NULL"))
            except Exception as e:
                logger.warning(f"Migration warning (users_auth email_verified_at): {e}")
        if "created_at" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"))
            except Exception as e:
                logger.warning(f"Migration warning (users_auth created_at): {e}")
        if "updated_at" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
            except Exception as e:
                logger.warning(f"Migration warning (users_auth updated_at): {e}")
    except Exception as e:
        logger.warning(f"Migration warning (users_auth): {e}")

    try:
        user_cols = [
            r["COLUMN_NAME"]
            for r in conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users'
            """)).mappings()
        ]
        user_alters = {
            "account_type": "ALTER TABLE users ADD COLUMN account_type ENUM('GUEST','USER') NOT NULL DEFAULT 'GUEST'",
            "status": "ALTER TABLE users ADD COLUMN status ENUM('ACTIVE','INACTIVE','BLOCKED') NOT NULL DEFAULT 'ACTIVE'",
            "invited_by": "ALTER TABLE users ADD COLUMN invited_by VARCHAR(255) NULL",
            "invitation_code": "ALTER TABLE users ADD COLUMN invitation_code VARCHAR(100) NULL",
            "converted_at": "ALTER TABLE users ADD COLUMN converted_at DATETIME NULL",
            "level": "ALTER TABLE users ADD COLUMN level VARCHAR(50) NULL",
            "position": "ALTER TABLE users ADD COLUMN position VARCHAR(50) NULL",
            "dominant_hand": "ALTER TABLE users ADD COLUMN dominant_hand ENUM('RIGHT','LEFT','BOTH') NULL",
            "deleted_at": "ALTER TABLE users ADD COLUMN deleted_at DATETIME NULL",
            "created_at": "ALTER TABLE users ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "ALTER TABLE users ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        }
        for col, stmt in user_alters.items():
            if col not in user_cols:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    logger.warning(f"Migration warning (users {col}): {e}")
    except Exception as e:
        logger.warning(f"Migration warning (users): {e}")

    try:
        match_cols = [
            r["COLUMN_NAME"]
            for r in conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'matches'
            """)).mappings()
        ]
        match_alters = {
            "round_id": "ALTER TABLE matches ADD COLUMN round_id VARCHAR(255) NULL",
            "business_id": "ALTER TABLE matches ADD COLUMN business_id VARCHAR(255) NULL",
            "court_id": "ALTER TABLE matches ADD COLUMN court_id VARCHAR(255) NULL",
            "created_by": "ALTER TABLE matches ADD COLUMN created_by VARCHAR(255) NOT NULL DEFAULT ''",
            "pair_a_id": "ALTER TABLE matches ADD COLUMN pair_a_id VARCHAR(255) NULL",
            "pair_b_id": "ALTER TABLE matches ADD COLUMN pair_b_id VARCHAR(255) NULL",
            "visibility": "ALTER TABLE matches ADD COLUMN visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PRIVATE'",
            "current_set_index": "ALTER TABLE matches ADD COLUMN current_set_index INT NOT NULL DEFAULT 0",
            "winner_pair_id": "ALTER TABLE matches ADD COLUMN winner_pair_id VARCHAR(255) NULL",
            "winner_team": "ALTER TABLE matches ADD COLUMN winner_team ENUM('A','B') NULL",
            "start_time_ms": "ALTER TABLE matches ADD COLUMN start_time_ms BIGINT NULL",
            "elapsed_time_sec": "ALTER TABLE matches ADD COLUMN elapsed_time_sec INT NOT NULL DEFAULT 0",
            "golden_point": "ALTER TABLE matches ADD COLUMN golden_point TINYINT(1) NOT NULL DEFAULT 0",
            "sets_to_win": "ALTER TABLE matches ADD COLUMN sets_to_win INT NOT NULL DEFAULT 2",
            "round_name": "ALTER TABLE matches ADD COLUMN round_name VARCHAR(100) NULL",
            "deleted_at": "ALTER TABLE matches ADD COLUMN deleted_at DATETIME NULL",
            "created_at": "ALTER TABLE matches ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "ALTER TABLE matches ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        }
        for col, stmt in match_alters.items():
            if col not in match_cols:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    logger.warning(f"Migration warning (matches {col}): {e}")
    except Exception as e:
        logger.warning(f"Migration warning (matches): {e}")

    try:
        pair_cols = [
            r["COLUMN_NAME"]
            for r in conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'pairs'
            """)).mappings()
        ]
        pair_alters = {
            "name": "ALTER TABLE pairs ADD COLUMN name VARCHAR(150) NULL",
            "created_by": "ALTER TABLE pairs ADD COLUMN created_by VARCHAR(255) NOT NULL DEFAULT ''",
            "tournaments_disputed": "ALTER TABLE pairs ADD COLUMN tournaments_disputed INT NOT NULL DEFAULT 0",
            "titles_won": "ALTER TABLE pairs ADD COLUMN titles_won INT NOT NULL DEFAULT 0",
            "created_at": "ALTER TABLE pairs ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "ALTER TABLE pairs ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        }
        for col, stmt in pair_alters.items():
            if col not in pair_cols:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    logger.warning(f"Migration warning (pairs {col}): {e}")
    except Exception as e:
        logger.warning(f"Migration warning (pairs): {e}")

    try:
        court_cols = [
            r["COLUMN_NAME"]
            for r in conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courts'
            """)).mappings()
        ]
        court_alters = {
            "business_id": "ALTER TABLE courts ADD COLUMN business_id VARCHAR(255) NOT NULL DEFAULT 'biz_default'",
            "location": "ALTER TABLE courts ADD COLUMN location TEXT NULL",
            "number": "ALTER TABLE courts ADD COLUMN number INT NULL",
            "created_at": "ALTER TABLE courts ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "ALTER TABLE courts ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        }
        for col, stmt in court_alters.items():
            if col not in court_cols:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    logger.warning(f"Migration warning (courts {col}): {e}")
    except Exception as e:
        logger.warning(f"Migration warning (courts): {e}")

    try:
        tournament_cols = [
            r["COLUMN_NAME"]
            for r in conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tournaments'
            """)).mappings()
        ]
        tournament_alters = {
            "business_id": "ALTER TABLE tournaments ADD COLUMN business_id VARCHAR(255) NULL",
            "created_by": "ALTER TABLE tournaments ADD COLUMN created_by VARCHAR(255) NOT NULL DEFAULT ''",
            "logo": "ALTER TABLE tournaments ADD COLUMN logo TEXT NULL",
            "description": "ALTER TABLE tournaments ADD COLUMN description TEXT NULL",
            "category": "ALTER TABLE tournaments ADD COLUMN category VARCHAR(100) NULL",
            "level": "ALTER TABLE tournaments ADD COLUMN level VARCHAR(100) NULL",
            "location": "ALTER TABLE tournaments ADD COLUMN location TEXT NULL",
            "format": "ALTER TABLE tournaments ADD COLUMN format VARCHAR(100) NULL",
            "max_pairs": "ALTER TABLE tournaments ADD COLUMN max_pairs INT NULL",
            "visibility": "ALTER TABLE tournaments ADD COLUMN visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PRIVATE'",
            "rules": "ALTER TABLE tournaments ADD COLUMN rules JSON NULL",
            "deleted_at": "ALTER TABLE tournaments ADD COLUMN deleted_at DATETIME NULL",
            "created_at": "ALTER TABLE tournaments ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "ALTER TABLE tournaments ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        }
        for col, stmt in tournament_alters.items():
            if col not in tournament_cols:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    logger.warning(f"Migration warning (tournaments {col}): {e}")
    except Exception as e:
        logger.warning(f"Migration warning (tournaments): {e}")

    try:
        notif_cols = [
            r["COLUMN_NAME"]
            for r in conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'notifications'
            """)).mappings()
        ]
        notif_alters = {
            "read_status": "ALTER TABLE notifications ADD COLUMN read_status TINYINT(1) NOT NULL DEFAULT 0",
            "type": "ALTER TABLE notifications ADD COLUMN type VARCHAR(100) NULL",
            "link_id": "ALTER TABLE notifications ADD COLUMN link_id VARCHAR(255) NULL",
            "created_at": "ALTER TABLE notifications ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
        }
        for col, stmt in notif_alters.items():
            if col not in notif_cols:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    logger.warning(f"Migration warning (notifications {col}): {e}")
    except Exception as e:
        logger.warning(f"Migration warning (notifications): {e}")
