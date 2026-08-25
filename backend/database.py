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
            id VARCHAR(255) PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            avatar TEXT,
            level TEXT,
            position TEXT,
            dominant_hand TEXT,
            current_pair_id TEXT,
            points INTEGER DEFAULT 0,
            partner_name TEXT,
            phone TEXT,
            stats TEXT
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pairs (
            id VARCHAR(255) PRIMARY KEY,
            name TEXT NOT NULL,
            player1_id TEXT NOT NULL,
            player2_id TEXT NOT NULL,
            player1_name TEXT NOT NULL,
            player2_name TEXT NOT NULL,
            player1_avatar TEXT,
            player2_avatar TEXT,
            created_at TEXT,
            status TEXT NOT NULL,
            tournaments_disputed INTEGER,
            titles_won INTEGER
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS courts (
            id VARCHAR(255) PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            number INTEGER NOT NULL,
            status TEXT NOT NULL,
            current_match_id TEXT
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tournaments (
            id VARCHAR(255) PRIMARY KEY,
            name TEXT NOT NULL,
            logo TEXT,
            description TEXT,
            category TEXT,
            level TEXT,
            location TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT,
            format TEXT,
            max_pairs INTEGER,
            registered_pair_ids TEXT,
            registered_user_ids TEXT,
            rules TEXT,
            court_ids TEXT
        )
    """))
    conn.execute(text("""
        ALTER TABLE tournaments
        ADD COLUMN IF NOT EXISTS registered_user_ids TEXT
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS matches (
            id VARCHAR(255) PRIMARY KEY,
            tournament_id TEXT,
            tournament_name TEXT,
            court_id TEXT,
            court_name TEXT NOT NULL,
            date_time TEXT NOT NULL,
            pair_a_id TEXT NOT NULL,
            pair_b_id TEXT NOT NULL,
            pair_a_name TEXT NOT NULL,
            pair_b_name TEXT NOT NULL,
            player_a1_id TEXT NOT NULL,
            player_a2_id TEXT NOT NULL,
            player_b1_id TEXT NOT NULL,
            player_b2_id TEXT NOT NULL,
            player_a1_name TEXT NOT NULL,
            player_a2_name TEXT NOT NULL,
            player_b1_name TEXT NOT NULL,
            player_b2_name TEXT NOT NULL,
            player_a1_avatar TEXT,
            player_a2_avatar TEXT,
            player_b1_avatar TEXT,
            player_b2_avatar TEXT,
            status TEXT NOT NULL,
            sets TEXT,
            current_game TEXT,
            current_set_index INTEGER,
            winner_pair_id TEXT,
            winner_team TEXT,
            start_time_ms INTEGER,
            elapsed_time_sec INTEGER NOT NULL,
            golden_point INTEGER NOT NULL,
            sets_to_win INTEGER NOT NULL,
            round_name TEXT
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id VARCHAR(255) PRIMARY KEY,
            admin_name TEXT NOT NULL,
            admin_email TEXT NOT NULL,
            action TEXT NOT NULL,
            target TEXT NOT NULL,
            details TEXT,
            timestamp TEXT NOT NULL
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS notifications (
            id VARCHAR(255) PRIMARY KEY,
            title TEXT NOT NULL,
            body TEXT,
            timestamp TEXT NOT NULL,
            `read` INTEGER NOT NULL,
            `type` TEXT NOT NULL,
            link_id TEXT
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS match_events (
            id VARCHAR(255) PRIMARY KEY,
            match_id TEXT NOT NULL,
            set_number INTEGER NOT NULL,
            game_number INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            winning_pair_id TEXT NOT NULL,
            player_id TEXT,
            player_name TEXT,
            event_type TEXT NOT NULL,
            description TEXT,
            score_snapshot TEXT
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS gesture_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            point_team_a_gesture TEXT NOT NULL,
            point_team_b_gesture TEXT NOT NULL,
            undo_gesture TEXT NOT NULL,
            cooldown_ms INTEGER NOT NULL,
            min_confidence REAL NOT NULL,
            required_hold_frames INTEGER NOT NULL,
            detection_zone TEXT,
            mode TEXT NOT NULL
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users_auth (
            id VARCHAR(255) PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """))

def seed_data(conn, data):
    for user in data["players"]:
        conn.execute(text("""
            INSERT INTO users (id, name, surname, username, email, role, avatar, level,
                position, dominant_hand, current_pair_id, points, partner_name, phone, stats)
            VALUES (:id, :name, :surname, :username, :email, :role, :avatar, :level,
                :position, :dominant_hand, :current_pair_id, :points, :partner_name, :phone, :stats)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), surname = VALUES(surname), username = VALUES(username),
                email = VALUES(email), role = VALUES(role), avatar = VALUES(avatar),
                level = VALUES(level), position = VALUES(position),
                dominant_hand = VALUES(dominant_hand), current_pair_id = VALUES(current_pair_id),
                points = VALUES(points), partner_name = VALUES(partner_name),
                phone = VALUES(phone), stats = VALUES(stats)
        """), {
            "id": user["id"], "name": user["name"], "surname": user["surname"],
            "username": user["username"], "email": user["email"], "role": user["role"],
            "avatar": user.get("avatar"), "level": user.get("level"),
            "position": user.get("position"), "dominant_hand": user.get("dominant_hand"),
            "current_pair_id": user.get("current_pair_id"), "points": user.get("points", 0),
            "partner_name": user.get("partner_name"), "phone": user.get("phone"),
            "stats": json.dumps(user.get("stats", {})),
        })

    for pair in data["pairs"]:
        conn.execute(text("""
            INSERT INTO pairs (id, name, player1_id, player2_id, player1_name, player2_name,
                player1_avatar, player2_avatar, created_at, status, tournaments_disputed, titles_won)
            VALUES (:id, :name, :player1_id, :player2_id, :player1_name, :player2_name,
                :player1_avatar, :player2_avatar, :created_at, :status, :tournaments_disputed, :titles_won)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id),
                player1_name = VALUES(player1_name), player2_name = VALUES(player2_name),
                player1_avatar = VALUES(player1_avatar), player2_avatar = VALUES(player2_avatar),
                created_at = VALUES(created_at), status = VALUES(status),
                tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won)
        """), {
            "id": pair["id"], "name": pair["name"], "player1_id": pair["player1_id"],
            "player2_id": pair["player2_id"], "player1_name": pair["player1_name"],
            "player2_name": pair["player2_name"], "player1_avatar": pair.get("player1_avatar"),
            "player2_avatar": pair.get("player2_avatar"), "created_at": pair.get("created_at"),
            "status": pair["status"], "tournaments_disputed": pair.get("tournaments_disputed"),
            "titles_won": pair.get("titles_won"),
        })

    for court in data["courts"]:
        conn.execute(text("""
            INSERT INTO courts (id, name, location, number, status, current_match_id)
            VALUES (:id, :name, :location, :number, :status, :current_match_id)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), location = VALUES(location), number = VALUES(number),
                status = VALUES(status), current_match_id = VALUES(current_match_id)
        """), {
            "id": court["id"], "name": court["name"], "location": court["location"],
            "number": court["number"], "status": court["status"],
            "current_match_id": court.get("current_match_id"),
        })

    for t in data["tournaments"]:
        conn.execute(text("""
            INSERT INTO tournaments (id, name, logo, description, category, level, location,
                start_date, end_date, status, format, max_pairs, registered_pair_ids, registered_user_ids, rules, court_ids)
            VALUES (:id, :name, :logo, :description, :category, :level, :location,
                :start_date, :end_date, :status, :format, :max_pairs, :registered_pair_ids, :registered_user_ids, :rules, :court_ids)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), logo = VALUES(logo), description = VALUES(description),
                category = VALUES(category), level = VALUES(level), location = VALUES(location),
                start_date = VALUES(start_date), end_date = VALUES(end_date), status = VALUES(status),
                format = VALUES(format), max_pairs = VALUES(max_pairs),
                registered_pair_ids = VALUES(registered_pair_ids), registered_user_ids = VALUES(registered_user_ids), rules = VALUES(rules), court_ids = VALUES(court_ids)
        """), {
            "id": t["id"], "name": t["name"], "logo": t.get("logo"), "description": t.get("description"),
            "category": t.get("category"), "level": t.get("level"), "location": t.get("location"),
            "start_date": t.get("start_date"), "end_date": t.get("end_date"), "status": t.get("status"),
            "format": t.get("format"), "max_pairs": t.get("max_pairs"),
            "registered_pair_ids": json.dumps(t.get("registered_pair_ids", [])),
            "registered_user_ids": json.dumps(t.get("registered_user_ids", [])),
            "rules": json.dumps(t.get("rules", {})),
            "court_ids": json.dumps(t.get("court_ids", [])),
        })

    for m in data["matches"]:
        conn.execute(text("""
            INSERT INTO matches (id, tournament_id, tournament_name, court_id, court_name, date_time,
                pair_a_id, pair_b_id, pair_a_name, pair_b_name, player_a1_id, player_a2_id,
                player_b1_id, player_b2_id, player_a1_name, player_a2_name, player_b1_name,
                player_b2_name, player_a1_avatar, player_a2_avatar, player_b1_avatar, player_b2_avatar,
                status, sets, current_game, current_set_index, winner_pair_id, winner_team,
                start_time_ms, elapsed_time_sec, golden_point, sets_to_win, round_name)
            VALUES (:id, :tournament_id, :tournament_name, :court_id, :court_name, :date_time,
                :pair_a_id, :pair_b_id, :pair_a_name, :pair_b_name, :player_a1_id, :player_a2_id,
                :player_b1_id, :player_b2_id, :player_a1_name, :player_a2_name, :player_b1_name,
                :player_b2_name, :player_a1_avatar, :player_a2_avatar, :player_b1_avatar, :player_b2_avatar,
                :status, :sets, :current_game, :current_set_index, :winner_pair_id, :winner_team,
                :start_time_ms, :elapsed_time_sec, :golden_point, :sets_to_win, :round_name)
            ON DUPLICATE KEY UPDATE
                tournament_id = VALUES(tournament_id), tournament_name = VALUES(tournament_name),
                court_id = VALUES(court_id), court_name = VALUES(court_name), date_time = VALUES(date_time),
                pair_a_id = VALUES(pair_a_id), pair_b_id = VALUES(pair_b_id),
                pair_a_name = VALUES(pair_a_name), pair_b_name = VALUES(pair_b_name),
                player_a1_id = VALUES(player_a1_id), player_a2_id = VALUES(player_a2_id),
                player_b1_id = VALUES(player_b1_id), player_b2_id = VALUES(player_b2_id),
                player_a1_name = VALUES(player_a1_name), player_a2_name = VALUES(player_a2_name),
                player_b1_name = VALUES(player_b1_name), player_b2_name = VALUES(player_b2_name),
                player_a1_avatar = VALUES(player_a1_avatar), player_a2_avatar = VALUES(player_a2_avatar),
                player_b1_avatar = VALUES(player_b1_avatar), player_b2_avatar = VALUES(player_b2_avatar),
                status = VALUES(status), sets = VALUES(sets), current_game = VALUES(current_game),
                current_set_index = VALUES(current_set_index), winner_pair_id = VALUES(winner_pair_id),
                winner_team = VALUES(winner_team), start_time_ms = VALUES(start_time_ms),
                elapsed_time_sec = VALUES(elapsed_time_sec), golden_point = VALUES(golden_point),
                sets_to_win = VALUES(sets_to_win), round_name = VALUES(round_name)
        """), {
            "id": m["id"], "tournament_id": m.get("tournament_id"),
            "tournament_name": m.get("tournament_name"), "court_id": m.get("court_id"),
            "court_name": m["court_name"], "date_time": m["date_time"],
            "pair_a_id": m["pair_a_id"], "pair_b_id": m["pair_b_id"],
            "pair_a_name": m["pair_a_name"], "pair_b_name": m["pair_b_name"],
            "player_a1_id": m["player_a1_id"], "player_a2_id": m["player_a2_id"],
            "player_b1_id": m["player_b1_id"], "player_b2_id": m["player_b2_id"],
            "player_a1_name": m["player_a1_name"], "player_a2_name": m["player_a2_name"],
            "player_b1_name": m["player_b1_name"], "player_b2_name": m["player_b2_name"],
            "player_a1_avatar": m.get("player_a1_avatar"), "player_a2_avatar": m.get("player_a2_avatar"),
            "player_b1_avatar": m.get("player_b1_avatar"), "player_b2_avatar": m.get("player_b2_avatar"),
            "status": m["status"], "sets": json.dumps(m.get("sets", [])),
            "current_game": json.dumps(m.get("current_game", {})),
            "current_set_index": m.get("current_set_index", 0),
            "winner_pair_id": m.get("winner_pair_id"), "winner_team": m.get("winner_team"),
            "start_time_ms": m.get("start_time_ms"),
            "elapsed_time_sec": m.get("elapsed_time_sec", 0),
            "golden_point": m.get("golden_point", False),
            "sets_to_win": m.get("sets_to_win", 2),
            "round_name": m.get("round_name"),
        })

    for log in data["audit_logs"]:
        conn.execute(text("""
            INSERT INTO audit_logs (id, admin_name, admin_email, action, target, details, timestamp)
            VALUES (:id, :admin_name, :admin_email, :action, :target, :details, :timestamp)
            ON DUPLICATE KEY UPDATE
                admin_name = VALUES(admin_name), admin_email = VALUES(admin_email),
                action = VALUES(action), target = VALUES(target),
                details = VALUES(details), timestamp = VALUES(timestamp)
        """), {
            "id": log["id"], "admin_name": log["admin_name"], "admin_email": log["admin_email"],
            "action": log["action"], "target": log["target"], "details": log.get("details"),
            "timestamp": log["timestamp"],
        })

    for notif in data["notifications"]:
        conn.execute(text("""
            INSERT INTO notifications (id, title, body, timestamp, `read`, `type`, link_id)
            VALUES (:id, :title, :body, :timestamp, :read, :type, :link_id)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title), body = VALUES(body), timestamp = VALUES(timestamp),
                `read` = VALUES(`read`), `type` = VALUES(`type`), link_id = VALUES(link_id)
        """), {
            "id": notif["id"], "title": notif["title"], "body": notif.get("body"),
            "timestamp": notif["timestamp"], "read": notif.get("read", False),
            "type": notif["type"], "link_id": notif.get("link_id"),
        })

    gc = data["gesture_configuration"]
    conn.execute(text("""
        INSERT INTO gesture_config (id, point_team_a_gesture, point_team_b_gesture,
            undo_gesture, cooldown_ms,
            min_confidence, required_hold_frames, detection_zone, mode)
        VALUES (1, :point_team_a_gesture, :point_team_b_gesture, :undo_gesture,
            :cooldown_ms,
            :min_confidence, :required_hold_frames, :detection_zone, :mode)
        ON DUPLICATE KEY UPDATE
            point_team_a_gesture = VALUES(point_team_a_gesture),
            point_team_b_gesture = VALUES(point_team_b_gesture),
            undo_gesture = VALUES(undo_gesture),
            cooldown_ms = VALUES(cooldown_ms),
            min_confidence = VALUES(min_confidence),
            required_hold_frames = VALUES(required_hold_frames),
            detection_zone = VALUES(detection_zone),
            mode = VALUES(mode)
    """), {
        "point_team_a_gesture": gc["point_team_a_gesture"],
        "point_team_b_gesture": gc["point_team_b_gesture"],
        "undo_gesture": gc["undo_gesture"],
        "cooldown_ms": gc["cooldown_ms"],
        "min_confidence": gc["min_confidence"],
        "required_hold_frames": gc["required_hold_frames"],
        "detection_zone": json.dumps(gc["detection_zone"]),
        "mode": gc["mode"],
    })

    auth_users = data.get("auth_users", [])
    for auth_user in auth_users:
        hashed = bcrypt.hashpw(auth_user["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn.execute(text("""
            INSERT INTO users_auth (id, email, hashed_password, role)
            VALUES (:id, :email, :hashed_password, :role)
            ON DUPLICATE KEY UPDATE
                email = VALUES(email),
                hashed_password = VALUES(hashed_password),
                role = VALUES(role)
        """), {
            "id": auth_user["id"],
            "email": auth_user["email"],
            "hashed_password": hashed,
            "role": auth_user["role"],
        })


def init_db():
    with engine.begin() as conn:
        create_schema(conn)
        data = load_mock_data()
        seed_data(conn, data)
    print("[db] Database initialized and seeded successfully.")
    return engine
