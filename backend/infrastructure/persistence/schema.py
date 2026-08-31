from sqlalchemy import text


def create_schema(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) NOT NULL,
            name VARCHAR(100) NOT NULL,
            surname VARCHAR(100) NULL,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(255) NULL,
            avatar TEXT NULL,
            account_type ENUM('GUEST','USER') NOT NULL DEFAULT 'GUEST',
            status ENUM('ACTIVE','INACTIVE','BLOCKED') NOT NULL DEFAULT 'ACTIVE',
            invited_by VARCHAR(255) NULL,
            invitation_code VARCHAR(100) NULL,
            converted_at DATETIME NULL,
            level VARCHAR(50) NULL,
            position VARCHAR(50) NULL,
            dominant_hand ENUM('RIGHT','LEFT','BOTH') NULL,
            points INT NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            deleted_at DATETIME NULL,
            PRIMARY KEY (id),
            UNIQUE KEY uk_users_username (username),
            UNIQUE KEY uk_users_email (email),
            UNIQUE KEY uk_users_invitation_code (invitation_code),
            INDEX idx_users_invited_by (invited_by),
            INDEX idx_users_account_type (account_type),
            INDEX idx_users_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users_auth (
            user_id VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            hashed_password VARCHAR(255) NULL,
            last_login DATETIME NULL,
            email_verified_at DATETIME NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id),
            UNIQUE KEY uk_users_auth_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS roles (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            description VARCHAR(255) NULL,
            PRIMARY KEY (id),
            UNIQUE KEY uk_roles_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id VARCHAR(255) NOT NULL,
            role_id INT UNSIGNED NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, role_id),
            INDEX idx_user_roles_role (role_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS profiles (
            user_id VARCHAR(255) NOT NULL,
            bio TEXT NULL,
            birth_date DATE NULL,
            city VARCHAR(100) NULL,
            country VARCHAR(100) NULL,
            preferred_position ENUM('RIGHT','LEFT','BOTH') NULL,
            skill_level ENUM('BEGINNER','INTERMEDIATE','ADVANCED','PRO') NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS privacy_settings (
            user_id VARCHAR(255) NOT NULL,
            profile_visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
            points_visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
            games_visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
            tournaments_visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS businesses (
            id VARCHAR(255) NOT NULL,
            name VARCHAR(200) NOT NULL,
            logo TEXT NULL,
            description TEXT NULL,
            location TEXT NULL,
            phone VARCHAR(50) NULL,
            email VARCHAR(255) NULL,
            created_by VARCHAR(255) NOT NULL,
            status ENUM('ACTIVE','INACTIVE') NOT NULL DEFAULT 'ACTIVE',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            deleted_at DATETIME NULL,
            PRIMARY KEY (id),
            INDEX idx_business_created_by (created_by)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS business_users (
            business_id VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            role ENUM('OWNER','ADMIN','MANAGER') NOT NULL DEFAULT 'MANAGER',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (business_id, user_id),
            INDEX idx_business_users_user (user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS gesture_config (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            business_id VARCHAR(255) NOT NULL,
            point_team_a_gesture TEXT NULL,
            point_team_b_gesture TEXT NULL,
            undo_gesture TEXT NULL,
            cooldown_ms INT NOT NULL DEFAULT 1000,
            min_confidence DOUBLE NOT NULL DEFAULT 0.80,
            required_hold_frames INT NOT NULL DEFAULT 10,
            detection_zone TEXT NULL,
            mode TEXT NULL,
            pause_timer_gesture TEXT NULL,
            resume_timer_gesture TEXT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY uk_gesture_business (business_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS courts (
            id VARCHAR(255) NOT NULL,
            business_id VARCHAR(255) NOT NULL,
            name VARCHAR(150) NOT NULL,
            location TEXT NULL,
            number INT NULL,
            status ENUM('AVAILABLE','OCCUPIED','MAINTENANCE','INACTIVE') NOT NULL DEFAULT 'AVAILABLE',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_courts_business (business_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pairs (
            id VARCHAR(255) NOT NULL,
            name VARCHAR(150) NULL,
            player1_id VARCHAR(255) NOT NULL,
            player2_id VARCHAR(255) NOT NULL,
            created_by VARCHAR(255) NOT NULL,
            status ENUM('ACTIVE','INACTIVE') NOT NULL DEFAULT 'ACTIVE',
            tournaments_disputed INT NOT NULL DEFAULT 0,
            titles_won INT NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_pairs_player1 (player1_id),
            INDEX idx_pairs_player2 (player2_id),
            INDEX idx_pairs_created_by (created_by),
            CONSTRAINT chk_pair_different_players CHECK (player1_id <> player2_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tournaments (
            id VARCHAR(255) NOT NULL,
            business_id VARCHAR(255) NULL,
            created_by VARCHAR(255) NOT NULL,
            name VARCHAR(200) NOT NULL,
            logo TEXT NULL,
            description TEXT NULL,
            category VARCHAR(100) NULL,
            level VARCHAR(100) NULL,
            location TEXT NULL,
            start_date DATETIME NOT NULL,
            end_date DATETIME NULL,
            format VARCHAR(100) NULL,
            max_pairs INT NULL,
            status ENUM('DRAFT','OPEN','IN_PROGRESS','FINISHED','CANCELLED') NOT NULL DEFAULT 'DRAFT',
            visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PRIVATE',
            rules JSON NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            deleted_at DATETIME NULL,
            PRIMARY KEY (id),
            INDEX idx_tournaments_business (business_id),
            INDEX idx_tournaments_created_by (created_by),
            INDEX idx_tournaments_status (status),
            INDEX idx_tournaments_visibility (visibility)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tournament_categories (
            id VARCHAR(255) NOT NULL,
            tournament_id VARCHAR(255) NOT NULL,
            name VARCHAR(100) NOT NULL,
            level VARCHAR(100) NULL,
            max_pairs INT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_tc_tournament (tournament_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tournament_rounds (
            id VARCHAR(255) NOT NULL,
            tournament_id VARCHAR(255) NOT NULL,
            category_id VARCHAR(255) NULL,
            name VARCHAR(100) NOT NULL,
            round_number INT NOT NULL,
            round_type ENUM('GROUP','ROUND_OF_32','ROUND_OF_16','QUARTERFINAL','SEMIFINAL','FINAL') NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_round_tournament (tournament_id),
            INDEX idx_round_category (category_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tournament_pairs (
            tournament_id VARCHAR(255) NOT NULL,
            pair_id VARCHAR(255) NOT NULL,
            category_id VARCHAR(255) NULL,
            seed INT NULL,
            status ENUM('REGISTERED','ACTIVE','ELIMINATED','CHAMPION','WITHDRAWN') NOT NULL DEFAULT 'REGISTERED',
            joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (tournament_id, pair_id),
            INDEX idx_tp_pair (pair_id),
            INDEX idx_tp_category (category_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tournament_players (
            tournament_id VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            category_id VARCHAR(255) NULL,
            status ENUM('REGISTERED','ACTIVE','ELIMINATED','WITHDRAWN','CHAMPION') NOT NULL DEFAULT 'REGISTERED',
            joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (tournament_id, user_id),
            INDEX idx_tournament_players_user (user_id),
            INDEX idx_tournament_players_category (category_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS matches (
            id VARCHAR(255) NOT NULL,
            tournament_id VARCHAR(255) NULL,
            round_id VARCHAR(255) NULL,
            business_id VARCHAR(255) NULL,
            court_id VARCHAR(255) NULL,
            created_by VARCHAR(255) NOT NULL,
            pair_a_id VARCHAR(255) NULL,
            pair_b_id VARCHAR(255) NULL,
            date_time DATETIME NULL,
            status ENUM('SCHEDULED','IN_PROGRESS','FINISHED','CANCELLED') NOT NULL DEFAULT 'SCHEDULED',
            visibility ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PRIVATE',
            sets JSON NULL,
            current_set_index INT NOT NULL DEFAULT 0,
            winner_pair_id VARCHAR(255) NULL,
            winner_team ENUM('A','B') NULL,
            start_time_ms BIGINT NULL,
            elapsed_time_sec INT NOT NULL DEFAULT 0,
            golden_point TINYINT(1) NOT NULL DEFAULT 0,
            sets_to_win INT NOT NULL DEFAULT 2,
            round_name VARCHAR(100) NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            deleted_at DATETIME NULL,
            PRIMARY KEY (id),
            INDEX idx_matches_tournament (tournament_id),
            INDEX idx_matches_round (round_id),
            INDEX idx_matches_business (business_id),
            INDEX idx_matches_court (court_id),
            INDEX idx_matches_created_by (created_by),
            INDEX idx_matches_pair_a (pair_a_id),
            INDEX idx_matches_pair_b (pair_b_id),
            INDEX idx_matches_winner_pair (winner_pair_id),
            INDEX idx_matches_status (status),
            INDEX idx_matches_date_time (date_time)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS match_players (
            match_id VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            pair_id VARCHAR(255) NULL,
            team ENUM('A','B') NOT NULL,
            player_number TINYINT UNSIGNED NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (match_id, user_id),
            INDEX idx_match_players_user (user_id),
            INDEX idx_match_players_pair (pair_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS match_events (
            id VARCHAR(255) NOT NULL,
            match_id VARCHAR(255) NOT NULL,
            set_number INT NOT NULL,
            game_number INT NULL,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            winning_pair_id VARCHAR(255) NULL,
            player_id VARCHAR(255) NULL,
            event_type VARCHAR(100) NOT NULL,
            description TEXT NULL,
            score_snapshot JSON NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_match_events_match (match_id),
            INDEX idx_match_events_player (player_id),
            INDEX idx_match_events_pair (winning_pair_id),
            INDEX idx_match_events_timestamp (timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS user_points (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            user_id VARCHAR(255) NOT NULL,
            match_id VARCHAR(255) NULL,
            tournament_id VARCHAR(255) NULL,
            points INT NOT NULL,
            reason VARCHAR(255) NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_user_points_user (user_id),
            INDEX idx_user_points_match (match_id),
            INDEX idx_user_points_tournament (tournament_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS notifications (
            id VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            body TEXT NULL,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            read_status TINYINT(1) NOT NULL DEFAULT 0,
            type VARCHAR(100) NULL,
            link_id VARCHAR(255) NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_notifications_user (user_id),
            INDEX idx_notifications_read (read_status),
            INDEX idx_notifications_timestamp (timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id VARCHAR(255) NOT NULL,
            business_id VARCHAR(255) NULL,
            user_id VARCHAR(255) NULL,
            action VARCHAR(100) NOT NULL,
            target_type VARCHAR(100) NOT NULL,
            target_id VARCHAR(255) NOT NULL,
            details JSON NULL,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            INDEX idx_audit_business (business_id),
            INDEX idx_audit_user (user_id),
            INDEX idx_audit_target (target_type, target_id),
            INDEX idx_audit_timestamp (timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """))


def _constraint_exists(conn, table_name, constraint_name):
    try:
        result = conn.execute(text("""
            SELECT COUNT(*) as cnt FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = :table_name
            AND CONSTRAINT_NAME = :constraint_name
        """), {"table_name": table_name, "constraint_name": constraint_name})
        row = result.mappings().first()
        return row and row["cnt"] > 0
    except Exception:
        return False


def _add_fk_safe(conn, table_name, constraint_name, column_name, ref_table, ref_column):
    if _constraint_exists(conn, table_name, constraint_name):
        return
    try:
        conn.execute(text(f"""
            ALTER TABLE {table_name}
            ADD CONSTRAINT {constraint_name}
            FOREIGN KEY ({column_name}) REFERENCES {ref_table}({ref_column})
            ON DELETE CASCADE ON UPDATE CASCADE
        """))
    except Exception:
        pass


def _add_fk_safe_set_null(conn, table_name, constraint_name, column_name, ref_table, ref_column):
    if _constraint_exists(conn, table_name, constraint_name):
        return
    try:
        conn.execute(text(f"""
            ALTER TABLE {table_name}
            ADD CONSTRAINT {constraint_name}
            FOREIGN KEY ({column_name}) REFERENCES {ref_table}({ref_column})
            ON DELETE SET NULL ON UPDATE CASCADE
        """))
    except Exception:
        pass


def _add_fk_safe_restrict(conn, table_name, constraint_name, column_name, ref_table, ref_column):
    if _constraint_exists(conn, table_name, constraint_name):
        return
    try:
        conn.execute(text(f"""
            ALTER TABLE {table_name}
            ADD CONSTRAINT {constraint_name}
            FOREIGN KEY ({column_name}) REFERENCES {ref_table}({ref_column})
            ON DELETE RESTRICT ON UPDATE CASCADE
        """))
    except Exception:
        pass


def migrate_schema(conn):
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
                ALTER TABLE users_auth
                CHANGE COLUMN id user_id VARCHAR(255) NOT NULL
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

    _add_fk_safe(conn, "users_auth", "fk_users_auth_user", "user_id", "users", "id")
    _add_fk_safe(conn, "user_roles", "fk_user_roles_user", "user_id", "users", "id")
    _add_fk_safe(conn, "user_roles", "fk_user_roles_role", "role_id", "roles", "id")
    _add_fk_safe(conn, "profiles", "fk_profiles_user", "user_id", "users", "id")
    _add_fk_safe(conn, "privacy_settings", "fk_privacy_user", "user_id", "users", "id")
    _add_fk_safe_set_null(conn, "businesses", "fk_businesses_creator", "created_by", "users", "id")
    _add_fk_safe(conn, "business_users", "fk_bu_business", "business_id", "businesses", "id")
    _add_fk_safe(conn, "business_users", "fk_bu_user", "user_id", "users", "id")
    _add_fk_safe(conn, "gesture_config", "fk_gesture_business", "business_id", "businesses", "id")
    _add_fk_safe(conn, "courts", "fk_courts_business", "business_id", "businesses", "id")
    _add_fk_safe(conn, "pairs", "fk_pairs_player1", "player1_id", "users", "id")
    _add_fk_safe(conn, "pairs", "fk_pairs_player2", "player2_id", "users", "id")
    _add_fk_safe_set_null(conn, "pairs", "fk_pairs_creator", "created_by", "users", "id")
    _add_fk_safe_set_null(conn, "tournaments", "fk_tournaments_business", "business_id", "businesses", "id")
    _add_fk_safe_set_null(conn, "tournaments", "fk_tournaments_creator", "created_by", "users", "id")
    _add_fk_safe(conn, "tournament_categories", "fk_tc_tournament", "tournament_id", "tournaments", "id")
    _add_fk_safe(conn, "tournament_rounds", "fk_tr_tournament", "tournament_id", "tournaments", "id")
    _add_fk_safe_set_null(conn, "tournament_rounds", "fk_tr_category", "category_id", "tournament_categories", "id")
    _add_fk_safe(conn, "tournament_pairs", "fk_tp_tournament", "tournament_id", "tournaments", "id")
    _add_fk_safe(conn, "tournament_pairs", "fk_tp_pair", "pair_id", "pairs", "id")
    _add_fk_safe_set_null(conn, "tournament_pairs", "fk_tp_category", "category_id", "tournament_categories", "id")
    _add_fk_safe(conn, "tournament_players", "fk_tplayers_tournament", "tournament_id", "tournaments", "id")
    _add_fk_safe(conn, "tournament_players", "fk_tplayers_user", "user_id", "users", "id")
    _add_fk_safe_set_null(conn, "tournament_players", "fk_tplayers_category", "category_id", "tournament_categories", "id")
    _add_fk_safe_set_null(conn, "matches", "fk_matches_tournament", "tournament_id", "tournaments", "id")
    _add_fk_safe_set_null(conn, "matches", "fk_matches_court", "court_id", "courts", "id")
    _add_fk_safe_set_null(conn, "matches", "fk_matches_pair_a", "pair_a_id", "pairs", "id")
    _add_fk_safe_set_null(conn, "matches", "fk_matches_pair_b", "pair_b_id", "pairs", "id")
    _add_fk_safe_set_null(conn, "matches", "fk_matches_winner", "winner_pair_id", "pairs", "id")
    _add_fk_safe_set_null(conn, "matches", "fk_matches_creator", "created_by", "users", "id")
    _add_fk_safe(conn, "match_players", "fk_mp_match", "match_id", "matches", "id")
    _add_fk_safe(conn, "match_players", "fk_mp_user", "user_id", "users", "id")
    _add_fk_safe_set_null(conn, "match_players", "fk_mp_pair", "pair_id", "pairs", "id")
    _add_fk_safe(conn, "match_events", "fk_me_match", "match_id", "matches", "id")
    _add_fk_safe_set_null(conn, "match_events", "fk_me_winning_pair", "winning_pair_id", "pairs", "id")
    _add_fk_safe_set_null(conn, "match_events", "fk_me_player", "player_id", "users", "id")
    _add_fk_safe(conn, "user_points", "fk_up_user", "user_id", "users", "id")
    _add_fk_safe_set_null(conn, "user_points", "fk_up_match", "match_id", "matches", "id")
    _add_fk_safe_set_null(conn, "user_points", "fk_up_tournament", "tournament_id", "tournaments", "id")
    _add_fk_safe(conn, "notifications", "fk_notif_user", "user_id", "users", "id")
    _add_fk_safe_set_null(conn, "audit_logs", "fk_audit_business", "business_id", "businesses", "id")
    _add_fk_safe_set_null(conn, "audit_logs", "fk_audit_user", "user_id", "users", "id")

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
