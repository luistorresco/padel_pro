import os
import json
import bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Configure it in your environment variables."
    )

MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "mock_data.json")

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)


def load_mock_data():
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


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


def seed_roles(conn):
    conn.execute(text("""
        INSERT IGNORE INTO roles (name, description) VALUES
        ('USER', 'Usuario normal de la aplicación'),
        ('BUSINESS_ADMIN', 'Administrador de un negocio'),
        ('BUSINESS_MANAGER', 'Administrador o manager de un negocio'),
        ('SUPER_ADMIN', 'Administrador general de la plataforma')
    """))


def seed_data(conn, data):
    players = data.get("players", [])
    pairs = data.get("pairs", [])
    courts = data.get("courts", [])
    tournaments = data.get("tournaments", [])
    matches = data.get("matches", [])
    audit_logs = data.get("audit_logs", [])
    notifications = data.get("notifications", [])
    gesture_config = data.get("gesture_configuration", {})
    auth_users = data.get("auth_users", [])

    for user in players:
        conn.execute(text("""
            INSERT INTO users (id, name, surname, username, email, avatar, account_type, status,
                level, position, dominant_hand, points)
            VALUES (:id, :name, :surname, :username, :email, :avatar, 'USER', 'ACTIVE',
                :level, :position, :dominant_hand, :points)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), surname = VALUES(surname), username = VALUES(username),
                email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level),
                position = VALUES(position), dominant_hand = VALUES(dominant_hand),
                points = VALUES(points)
        """), {
            "id": user["id"], "name": user["name"], "surname": user.get("surname", ""),
            "username": user["username"], "email": user.get("email"),
            "avatar": user.get("avatar"), "level": user.get("level"),
            "position": user.get("position"), "dominant_hand": user.get("dominant_hand"),
            "points": user.get("points", 0),
        })

        if user.get("email"):
            conn.execute(text("""
                INSERT IGNORE INTO users_auth (user_id, email, hashed_password)
                VALUES (:user_id, :email, :hashed_password)
            """), {
                "user_id": user["id"],
                "email": user["email"],
                "hashed_password": bcrypt.hashpw(
                    (user.get("password") or "password").encode("utf-8"),
                    bcrypt.gensalt()
                ).decode("utf-8"),
            })

    for pair in pairs:
        conn.execute(text("""
            INSERT INTO pairs (id, name, player1_id, player2_id, created_by, status,
                tournaments_disputed, titles_won)
            VALUES (:id, :name, :player1_id, :player2_id, :created_by, :status,
                :tournaments_disputed, :titles_won)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id),
                status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed),
                titles_won = VALUES(titles_won)
        """), {
            "id": pair["id"], "name": pair.get("name"),
            "player1_id": pair["player1_id"], "player2_id": pair["player2_id"],
            "created_by": pair.get("created_by", pair["player1_id"]),
            "status": pair.get("status", "ACTIVE"),
            "tournaments_disputed": pair.get("tournaments_disputed", 0),
            "titles_won": pair.get("titles_won", 0),
        })

    for court in courts:
        conn.execute(text("""
            INSERT INTO courts (id, business_id, name, location, number, status)
            VALUES (:id, :business_id, :name, :location, :number, :status)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), location = VALUES(location), number = VALUES(number),
                status = VALUES(status)
        """), {
            "id": court["id"], "business_id": court.get("business_id", "biz_default"),
            "name": court["name"], "location": court.get("location"),
            "number": court.get("number"), "status": court.get("status", "AVAILABLE"),
        })

    for t in tournaments:
        conn.execute(text("""
            INSERT INTO tournaments (id, business_id, created_by, name, logo, description, category,
                level, location, start_date, end_date, status, format, max_pairs, visibility, rules)
            VALUES (:id, :business_id, :created_by, :name, :logo, :description, :category,
                :level, :location, :start_date, :end_date, :status, :format, :max_pairs, :visibility, :rules)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), description = VALUES(description), category = VALUES(category),
                level = VALUES(level), location = VALUES(location), start_date = VALUES(start_date),
                end_date = VALUES(end_date), status = VALUES(status), format = VALUES(format),
                max_pairs = VALUES(max_pairs), visibility = VALUES(visibility), rules = VALUES(rules)
        """), {
            "id": t["id"], "business_id": t.get("business_id"),
            "created_by": t.get("created_by", t.get("createdBy")), "name": t["name"],
            "logo": t.get("logo"), "description": t.get("description"),
            "category": t.get("category"), "level": t.get("level"),
            "location": t.get("location"), "start_date": t.get("start_date"),
            "end_date": t.get("end_date"), "status": t.get("status", "DRAFT"),
            "format": t.get("format"), "max_pairs": t.get("max_pairs"),
            "visibility": t.get("visibility", "PRIVATE"),
            "rules": json.dumps(t.get("rules", {})),
        })

    for m in matches:
        conn.execute(text("""
            INSERT INTO matches (id, tournament_id, court_id, date_time, pair_a_id, pair_b_id,
                status, sets, current_set_index, winner_pair_id, winner_team,
                start_time_ms, elapsed_time_sec, golden_point, sets_to_win, round_name, created_by)
            VALUES (:id, :tournament_id, :court_id, :date_time, :pair_a_id, :pair_b_id,
                :status, :sets, :current_set_index, :winner_pair_id, :winner_team,
                :start_time_ms, :elapsed_time_sec, :golden_point, :sets_to_win, :round_name, :created_by)
            ON DUPLICATE KEY UPDATE
                tournament_id = VALUES(tournament_id), court_id = VALUES(court_id),
                date_time = VALUES(date_time), pair_a_id = VALUES(pair_a_id),
                pair_b_id = VALUES(pair_b_id), status = VALUES(status),
                sets = VALUES(sets), current_set_index = VALUES(current_set_index),
                winner_pair_id = VALUES(winner_pair_id), winner_team = VALUES(winner_team),
                start_time_ms = VALUES(start_time_ms), elapsed_time_sec = VALUES(elapsed_time_sec),
                golden_point = VALUES(golden_point), sets_to_win = VALUES(sets_to_win),
                round_name = VALUES(round_name)
        """), {
            "id": m["id"], "tournament_id": m.get("tournament_id"),
            "court_id": m.get("court_id"), "date_time": m.get("date_time"),
            "pair_a_id": m.get("pair_a_id"), "pair_b_id": m.get("pair_b_id"),
            "status": m.get("status", "SCHEDULED"),
            "sets": json.dumps(m.get("sets", [])),
            "current_set_index": m.get("current_set_index", 0),
            "winner_pair_id": m.get("winner_pair_id"), "winner_team": m.get("winner_team"),
            "start_time_ms": m.get("start_time_ms"),
            "elapsed_time_sec": m.get("elapsed_time_sec", 0),
            "golden_point": 1 if m.get("golden_point") else 0,
            "sets_to_win": m.get("sets_to_win", 2),
            "round_name": m.get("round_name"),
            "created_by": m.get("created_by", "usr_001"),
        })

    for log in audit_logs:
        conn.execute(text("""
            INSERT INTO audit_logs (id, action, target_type, target_id, details, timestamp)
            VALUES (:id, :action, :target_type, :target_id, :details, :timestamp)
            ON DUPLICATE KEY UPDATE
                action = VALUES(action), target_type = VALUES(target_type),
                target_id = VALUES(target_id), details = VALUES(details),
                timestamp = VALUES(timestamp)
        """), {
            "id": log["id"], "action": log.get("action"),
            "target_type": log.get("target_type", "unknown"),
            "target_id": log.get("target_id", ""), "details": json.dumps(log.get("details", {})),
            "timestamp": log.get("timestamp"),
        })

    for notif in notifications:
        conn.execute(text("""
            INSERT INTO notifications (id, user_id, title, body, timestamp, read_status, type, link_id)
            VALUES (:id, :user_id, :title, :body, :timestamp, :read_status, :type, :link_id)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title), body = VALUES(body), read_status = VALUES(read_status),
                type = VALUES(type), link_id = VALUES(link_id)
        """), {
            "id": notif["id"], "user_id": notif.get("user_id", "usr_001"),
            "title": notif["title"], "body": notif.get("body"),
            "timestamp": notif.get("timestamp"), "read_status": 1 if notif.get("read") else 0,
            "type": notif.get("type"), "link_id": notif.get("link_id"),
        })

    if gesture_config:
        conn.execute(text("""
            INSERT INTO gesture_config (business_id, point_team_a_gesture, point_team_b_gesture,
                undo_gesture, cooldown_ms, min_confidence, required_hold_frames,
                detection_zone, mode, pause_timer_gesture, resume_timer_gesture)
            VALUES ('biz_default', :point_team_a_gesture, :point_team_b_gesture, :undo_gesture,
                :cooldown_ms, :min_confidence, :required_hold_frames,
                :detection_zone, :mode, :pause_timer_gesture, :resume_timer_gesture)
            ON DUPLICATE KEY UPDATE
                point_team_a_gesture = VALUES(point_team_a_gesture),
                point_team_b_gesture = VALUES(point_team_b_gesture),
                undo_gesture = VALUES(undo_gesture), cooldown_ms = VALUES(cooldown_ms),
                min_confidence = VALUES(min_confidence),
                required_hold_frames = VALUES(required_hold_frames),
                detection_zone = VALUES(detection_zone), mode = VALUES(mode),
                pause_timer_gesture = VALUES(pause_timer_gesture),
                resume_timer_gesture = VALUES(resume_timer_gesture)
        """), {
            "point_team_a_gesture": gesture_config.get("point_team_a_gesture"),
            "point_team_b_gesture": gesture_config.get("point_team_b_gesture"),
            "undo_gesture": gesture_config.get("undo_gesture"),
            "cooldown_ms": gesture_config.get("cooldown_ms", 1000),
            "min_confidence": gesture_config.get("min_confidence", 0.8),
            "required_hold_frames": gesture_config.get("required_hold_frames", 10),
            "detection_zone": json.dumps(gesture_config.get("detection_zone")),
            "mode": gesture_config.get("mode"),
            "pause_timer_gesture": gesture_config.get("pause_timer_gesture"),
            "resume_timer_gesture": gesture_config.get("resume_timer_gesture"),
        })

    seed_roles(conn)

    auth_users = data.get("auth_users", [])
    for auth_user in auth_users:
        hashed = bcrypt.hashpw(auth_user["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn.execute(text("""
            INSERT INTO users_auth (user_id, email, hashed_password)
            VALUES (:user_id, :email, :hashed_password)
            ON DUPLICATE KEY UPDATE
                email = VALUES(email),
                hashed_password = VALUES(hashed_password)
        """), {
            "user_id": auth_user["id"],
            "email": auth_user["email"],
            "hashed_password": hashed,
        })


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


def init_db():
    with engine.begin() as conn:
        create_schema(conn)
        migrate_schema(conn)
        result = conn.execute(text("SELECT COUNT(*) as cnt FROM users"))
        row = result.mappings().first()
        if row and row["cnt"] == 0:
            data = load_mock_data()
            seed_data(conn, data)
            print("[db] Database seeded with initial data.")
        else:
            print("[db] Database already contains data. Skipping seed.")
    print("[db] Database initialized successfully.")
    return engine
