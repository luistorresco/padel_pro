import json
import bcrypt
from sqlalchemy import text

from domain.value_objects.skill_level import SkillLevel
from domain.value_objects.dominant_hand import DominantHand
from domain.value_objects.match_status import MatchStatus
from domain.value_objects.tournament_status import TournamentStatus
from domain.value_objects.court_status import CourtStatus


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
        try:
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
                "avatar": user.get("avatar"), "level": SkillLevel.normalize(user.get("level")),
                "position": DominantHand.normalize(user.get("position")),
                "dominant_hand": DominantHand.normalize(user.get("dominant_hand")),
                "points": user.get("points", 0),
            })
        except Exception:
            pass

        if user.get("email"):
            try:
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
            except Exception:
                pass

    tournament_pairs_mock = data.get("tournament_pairs", [])
    for t in tournaments:
        pair_ids_for_tournament = t.get("registered_pair_ids", [])
        if not pair_ids_for_tournament:
            continue
        for pid in pair_ids_for_tournament:
            pair_exists = conn.execute(text("SELECT COUNT(*) as cnt FROM pairs WHERE id = :id"), {"id": pid}).mappings().first()
            if not pair_exists or pair_exists["cnt"] == 0:
                continue
            try:
                conn.execute(text("""
                    INSERT INTO tournament_pairs (tournament_id, pair_id, status)
                    VALUES (:tid, :pid, 'REGISTERED')
                    ON DUPLICATE KEY UPDATE status = VALUES(status)
                """), {"tid": t["id"], "pid": pid})
            except Exception:
                pass

    for t in tournaments:
        user_ids_for_tournament = t.get("registered_user_ids", [])
        if not user_ids_for_tournament:
            continue
        for uid in user_ids_for_tournament:
            user_exists = conn.execute(text("SELECT COUNT(*) as cnt FROM users WHERE id = :id"), {"id": uid}).mappings().first()
            if not user_exists or user_exists["cnt"] == 0:
                continue
            try:
                conn.execute(text("""
                    INSERT INTO tournament_players (tournament_id, user_id, status)
                    VALUES (:tid, :uid, 'REGISTERED')
                    ON DUPLICATE KEY UPDATE status = VALUES(status)
                """), {"tid": t["id"], "uid": uid})
            except Exception:
                pass

    for m in matches:
        match_id = m["id"]
        match_row = conn.execute(text("SELECT pair_a_id, pair_b_id FROM matches WHERE id = :id"), {"id": match_id}).mappings().first()
        if not match_row:
            continue
        for team, pair_id in [("A", match_row["pair_a_id"]), ("B", match_row["pair_b_id"])]:
            if not pair_id:
                continue
            pair = conn.execute(text("SELECT player1_id, player2_id FROM pairs WHERE id = :id"), {"id": pair_id}).mappings().first()
            if not pair:
                continue
            for idx, uid in enumerate([pair["player1_id"], pair["player2_id"]], 1):
                if not uid:
                    continue
                try:
                    conn.execute(text("""
                        INSERT INTO match_players (match_id, user_id, pair_id, team, player_number)
                        VALUES (:mid, :uid, :pid, :team, :pn)
                        ON DUPLICATE KEY UPDATE pair_id = VALUES(pair_id), team = VALUES(team)
                    """), {"mid": match_id, "uid": uid, "pid": pair_id, "team": team, "pn": idx})
                except Exception:
                    pass

    for pair in pairs:
        try:
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
        except Exception:
            pass

    for court in courts:
        try:
            conn.execute(text("""
                INSERT INTO courts (id, business_id, name, location, number, status)
                VALUES (:id, :business_id, :name, :location, :number, :status)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name), location = VALUES(location), number = VALUES(number),
                    status = VALUES(status)
            """), {
                "id": court["id"], "business_id": court.get("business_id", "biz_default"),
                "name": court["name"], "location": court.get("location"),
                "number": court.get("number"), "status": CourtStatus.normalize(court.get("status")),
            })
        except Exception:
            pass

    for t in tournaments:
        try:
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
                "created_by": t.get("created_by") or t.get("createdBy") or "usr_carlos_admin",
                "name": t["name"],
                "logo": t.get("logo"), "description": t.get("description"),
                "category": t.get("category"), "level": SkillLevel.normalize(t.get("level")),
                "location": t.get("location"), "start_date": t.get("start_date"),
                "end_date": t.get("end_date"), "status": TournamentStatus.normalize(t.get("status")),
                "format": t.get("format"), "max_pairs": t.get("max_pairs"),
                "visibility": t.get("visibility", "PRIVATE"),
                "rules": json.dumps(t.get("rules", {})),
            })
        except Exception:
            pass

    for m in matches:
        try:
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
                "status": MatchStatus.normalize(m.get("status")),
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
        except Exception:
            pass

    for log in audit_logs:
        try:
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
        except Exception:
            pass

    for notif in notifications:
        try:
            ts = notif.get("timestamp")
            import re
            if ts and not re.match(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$", str(ts).strip()):
                ts = None
            conn.execute(text("""
                INSERT INTO notifications (id, user_id, title, body, timestamp, read_status, type, link_id)
                VALUES (:id, :user_id, :title, :body, COALESCE(:timestamp, CURRENT_TIMESTAMP), :read_status, :type, :link_id)
                ON DUPLICATE KEY UPDATE
                    title = VALUES(title), body = VALUES(body), read_status = VALUES(read_status),
                    type = VALUES(type), link_id = VALUES(link_id)
            """), {
                "id": notif["id"], "user_id": notif.get("user_id", "usr_001"),
                "title": notif["title"], "body": notif.get("body"),
                "timestamp": ts, "read_status": 1 if notif.get("read") else 0,
                "type": notif.get("type"), "link_id": notif.get("link_id"),
            })
        except Exception:
            pass

    if gesture_config:
        try:
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
        except Exception:
            pass

    seed_roles(conn)

    auth_users = data.get("auth_users", [])
    for auth_user in auth_users:
        try:
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
        except Exception:
            pass

    players = data.get("players", [])
    role_mapping = {
        "ADMIN": "SUPER_ADMIN",
        "SUPER_ADMIN": "SUPER_ADMIN",
        "BUSINESS_ADMIN": "BUSINESS_ADMIN",
        "BUSINESS_MANAGER": "BUSINESS_MANAGER",
        "MANAGER": "BUSINESS_MANAGER",
        "USER": "USER",
        "PLAYER": "USER",
    }
    role_rows = conn.execute(text("SELECT id, name FROM roles")).mappings().all()
    role_map = {row["name"]: row["id"] for row in role_rows}
    for user in players:
        raw_role = user.get("role", "USER")
        mapped_role = role_mapping.get(raw_role, "USER")
        role_id = role_map.get(mapped_role)
        if not role_id:
            continue
        try:
            conn.execute(text("""
                INSERT INTO user_roles (user_id, role_id)
                VALUES (:user_id, :role_id)
                ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
            """), {"user_id": user["id"], "role_id": role_id})
        except Exception:
            pass
