"""Run database migrations."""

from sqlalchemy import text


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
            except Exception:
                pass
        if "last_login" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN last_login DATETIME NULL"))
            except Exception:
                pass
        if "email_verified_at" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN email_verified_at DATETIME NULL"))
            except Exception:
                pass
        if "created_at" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"))
            except Exception:
                pass
        if "updated_at" not in cols:
            try:
                conn.execute(text("ALTER TABLE users_auth ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
            except Exception:
                pass
    except Exception:
        pass

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
                except Exception:
                    pass
    except Exception:
        pass

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
                except Exception:
                    pass
    except Exception:
        pass
