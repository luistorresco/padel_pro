#!/usr/bin/env python3
"""
Full seed script for Padel Pro MySQL database.
Fills all empty tables while preserving existing data.
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                if key.strip() == "DATABASE_URL":
                    DATABASE_URL = value.strip().strip('"').strip("'")
                    break

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)


def _map_match_status(value):
    if not value:
        return "SCHEDULED"
    value = str(value).strip().upper()
    if value == "LIVE":
        return "IN_PROGRESS"
    if value == "UPCOMING":
        return "SCHEDULED"
    return value


def _map_position(value):
    if not value:
        return "RIGHT"
    v = str(value).lower()
    if "izquierda" in v or "left" in v or "revés" in v or "reves" in v:
        return "LEFT"
    if "derecha" in v or "right" in v or "drive" in v:
        return "RIGHT"
    if "ambas" in v or "both" in v:
        return "BOTH"
    return "RIGHT"


def _map_skill(value):
    if not value:
        return "INTERMEDIATE"
    v = str(value).lower()
    if "principiante" in v or "beginner" in v:
        return "BEGINNER"
    if "intermedio" in v or "intermediate" in v:
        return "INTERMEDIATE"
    if "avanzado" in v or "advanced" in v:
        return "ADVANCED"
    if "profesional" in v or "pro" in v:
        return "PRO"
    return "INTERMEDIATE"


def main():
    mock_data_path = os.path.join(os.path.dirname(__file__), "mock_data.json")
    with open(mock_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    users = data.get("players", [])
    pairs = data.get("pairs", [])
    tournaments = data.get("tournaments", [])
    matches = data.get("matches", [])
    auth_users = data.get("auth_users", [])

    with engine.begin() as conn:
        print("[seed_full] Starting full database seed...")

        # Create business if none exists
        result = conn.execute(text("SELECT COUNT(*) as cnt FROM businesses"))
        biz_count = result.mappings().first()["cnt"]
        if biz_count == 0:
            conn.execute(text("""
                INSERT INTO businesses (id, name, description, location, created_by, status)
                VALUES ('biz_default', 'Padel Pro Club', 'Club principal de padel', 'Madrid, España', 'usr_carlos_admin', 'ACTIVE')
                ON DUPLICATE KEY UPDATE name = VALUES(name)
            """))
            print("[seed_full] Business created.")

        # Seed profiles
        for user in users:
            try:
                conn.execute(text("""
                    INSERT INTO profiles (user_id, bio, birth_date, city, country, preferred_position, skill_level)
                    VALUES (:user_id, :bio, :birth_date, :city, :country, :preferred_position, :skill_level)
                    ON DUPLICATE KEY UPDATE bio = VALUES(bio), birth_date = VALUES(birth_date)
                """), {
                    "user_id": user["id"],
                    "bio": user.get("bio") or f"Jugador de padel - {user.get('name', '')}",
                    "birth_date": user.get("birth_date"),
                    "city": user.get("city", "Madrid"),
                    "country": user.get("country", "España"),
                    "preferred_position": _map_position(user.get("position")),
                    "skill_level": _map_skill(user.get("level")),
                })
            except Exception as e:
                print(f"[seed_full] Profile skip {user['id']}: {e}")

        # Seed privacy_settings
        for user in users:
            try:
                conn.execute(text("""
                    INSERT INTO privacy_settings (user_id, profile_visibility, points_visibility, games_visibility, tournaments_visibility)
                    VALUES (:user_id, 'PUBLIC', 'PUBLIC', 'PUBLIC', 'PUBLIC')
                    ON DUPLICATE KEY UPDATE profile_visibility = VALUES(profile_visibility)
                """), {"user_id": user["id"]})
            except Exception as e:
                print(f"[seed_full] Privacy skip {user['id']}: {e}")

        # Seed user_roles (from roles table + auth_users)
        result = conn.execute(text("SELECT id, name FROM roles"))
        role_map = {row["name"]: row["id"] for row in result.mappings()}
        role_mapping = {
            "ADMIN": "SUPER_ADMIN",
            "SUPER_ADMIN": "SUPER_ADMIN",
            "BUSINESS_ADMIN": "BUSINESS_ADMIN",
            "BUSINESS_MANAGER": "BUSINESS_MANAGER",
            "MANAGER": "BUSINESS_MANAGER",
            "USER": "USER",
            "PLAYER": "USER",
        }
        admin_assigned = False
        for user in users:
            raw_role = user.get("role", "USER")
            mapped_role = role_mapping.get(raw_role, "USER")
            if mapped_role in {"SUPER_ADMIN", "BUSINESS_ADMIN", "BUSINESS_MANAGER"}:
                admin_assigned = True
            role_id = role_map.get(mapped_role, role_map.get("USER"))
            if role_id:
                try:
                    conn.execute(text("""
                        INSERT INTO user_roles (user_id, role_id)
                        VALUES (:user_id, :role_id)
                        ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
                    """), {"user_id": user["id"], "role_id": role_id})
                except Exception as e:
                    print(f"[seed_full] User role skip {user['id']}: {e}")

        if not admin_assigned:
            super_admin_role_id = role_map.get("SUPER_ADMIN")
            if super_admin_role_id and users:
                try:
                    conn.execute(text("""
                        INSERT INTO user_roles (user_id, role_id)
                        VALUES (:user_id, :role_id)
                        ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
                    """), {"user_id": users[0]["id"], "role_id": super_admin_role_id})
                    print(f"[seed_full] Assigned SUPER_ADMIN to {users[0]['id']}")
                except Exception as e:
                    print(f"[seed_full] Super admin skip: {e}")

        # Ensure at least one dedicated admin user exists with SUPER_ADMIN role
        admin_email = "admin@padelpro.app"
        admin_name = "Admin User"
        existing_admin = conn.execute(text("""
            SELECT ua.user_id FROM users_auth ua
            JOIN user_roles ur ON ua.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.id
            WHERE r.name = 'SUPER_ADMIN'
            LIMIT 1
        """)).mappings().first()
        if not existing_admin:
            admin_id = "usr_admin_super"
            try:
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
                hashed = __import__('domain.services.auth_service', fromlist=['AuthService']).AuthService(secret_key="padel-pro-secret-key-change-in-production").hash_password("admin123")
                conn.execute(text("""
                    INSERT INTO users_auth (user_id, email, hashed_password)
                    VALUES (:user_id, :email, :hashed_password)
                    ON DUPLICATE KEY UPDATE email = VALUES(email), hashed_password = VALUES(hashed_password)
                """), {"user_id": admin_id, "email": admin_email, "hashed_password": hashed})
                if super_admin_role_id:
                    conn.execute(text("""
                        INSERT INTO user_roles (user_id, role_id)
                        VALUES (:user_id, :role_id)
                        ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
                    """), {"user_id": admin_id, "role_id": super_admin_role_id})
                print(f"[seed_full] Created dedicated admin user: {admin_email} / admin123")
            except Exception as e:
                print(f"[seed_full] Admin user creation skip: {e}")

        # Seed business_users
        for user in users:
            try:
                conn.execute(text("""
                    INSERT INTO business_users (business_id, user_id, role)
                    VALUES ('biz_default', :user_id, 'MANAGER')
                    ON DUPLICATE KEY UPDATE role = VALUES(role)
                """), {"user_id": user["id"]})
            except Exception as e:
                print(f"[seed_full] Business user skip {user['id']}: {e}")

        # Seed user_points
        for user in users:
            try:
                conn.execute(text("""
                    INSERT INTO user_points (user_id, match_id, tournament_id, points, reason)
                    VALUES (:user_id, NULL, NULL, :points, 'Initial points')
                    ON DUPLICATE KEY UPDATE points = VALUES(points)
                """), {"user_id": user["id"], "points": user.get("points", 0)})
            except Exception as e:
                print(f"[seed_full] User points skip {user['id']}: {e}")

        # Seed pairs (must be before tournament_pairs/matches)
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
                    "player1_id": pair.get("player1_id"), "player2_id": pair.get("player2_id"),
                    "created_by": pair.get("created_by", pair.get("player1_id")),
                    "status": pair.get("status", "ACTIVE"),
                    "tournaments_disputed": pair.get("tournaments_disputed", 0),
                    "titles_won": pair.get("titles_won", 0),
                })
            except Exception as e:
                print(f"[seed_full] Pair skip {pair['id']}: {e}")

        # Seed matches (must be before match_players/match_events)
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
                    "status": _map_match_status(m.get("status")),
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
            except Exception as e:
                print(f"[seed_full] Match skip {m['id']}: {e}")

        # Seed tournament_categories
        for t in tournaments:
            try:
                cat_id = f"cat_{t['id']}"
                conn.execute(text("""
                    INSERT INTO tournament_categories (id, tournament_id, name, level, max_pairs)
                    VALUES (:id, :tournament_id, :name, :level, :max_pairs)
                    ON DUPLICATE KEY UPDATE name = VALUES(name)
                """), {
                    "id": cat_id,
                    "tournament_id": t["id"],
                    "name": t.get("category") or "Main",
                    "level": t.get("level") or "PRO",
                    "max_pairs": t.get("max_pairs") or 16,
                })
            except Exception as e:
                print(f"[seed_full] Category skip {t['id']}: {e}")

        # Seed tournament_rounds
        round_types = ["GROUP", "ROUND_OF_16", "QUARTERFINAL", "SEMIFINAL", "FINAL"]
        for t in tournaments:
            cat_id = f"cat_{t['id']}"
            for i, rtype in enumerate(round_types, 1):
                try:
                    conn.execute(text("""
                        INSERT INTO tournament_rounds (id, tournament_id, category_id, name, round_number, round_type)
                        VALUES (:id, :tournament_id, :category_id, :name, :round_number, :round_type)
                        ON DUPLICATE KEY UPDATE name = VALUES(name)
                    """), {
                        "id": f"round_{t['id']}_{i}",
                        "tournament_id": t["id"],
                        "category_id": cat_id,
                        "name": rtype.replace("_", " ").title(),
                        "round_number": i,
                        "round_type": rtype,
                    })
                except Exception as e:
                    print(f"[seed_full] Round skip {t['id']}: {e}")

        # Seed tournament_pairs (only for pairs that exist)
        for t in tournaments:
            cat_id = f"cat_{t['id']}"
            registered_pair_ids = t.get("registered_pair_ids", [])
            for pid in registered_pair_ids:
                # Verify pair exists
                pair_check = conn.execute(text("SELECT COUNT(*) as cnt FROM pairs WHERE id = :id"), {"id": pid}).mappings().first()
                if not pair_check or pair_check["cnt"] == 0:
                    print(f"[seed_full] Skipping tournament pair {pid} (does not exist)")
                    continue
                try:
                    conn.execute(text("""
                        INSERT INTO tournament_pairs (tournament_id, pair_id, category_id, seed, status)
                        VALUES (:tournament_id, :pair_id, :category_id, :seed, 'REGISTERED')
                        ON DUPLICATE KEY UPDATE status = VALUES(status)
                    """), {
                        "tournament_id": t["id"],
                        "pair_id": pid,
                        "category_id": cat_id,
                        "seed": None,
                    })
                except Exception as e:
                    print(f"[seed_full] Tournament pair skip {pid}: {e}")

        # Seed tournament_players (only for users that exist)
        for t in tournaments:
            cat_id = f"cat_{t['id']}"
            registered_user_ids = t.get("registered_user_ids", [])
            for uid in registered_user_ids:
                user_check = conn.execute(text("SELECT COUNT(*) as cnt FROM users WHERE id = :id"), {"id": uid}).mappings().first()
                if not user_check or user_check["cnt"] == 0:
                    print(f"[seed_full] Skipping tournament player {uid} (does not exist)")
                    continue
                try:
                    conn.execute(text("""
                        INSERT INTO tournament_players (tournament_id, user_id, category_id, status)
                        VALUES (:tournament_id, :user_id, :category_id, 'REGISTERED')
                        ON DUPLICATE KEY UPDATE status = VALUES(status)
                    """), {
                        "tournament_id": t["id"],
                        "user_id": uid,
                        "category_id": cat_id,
                    })
                except Exception as e:
                    print(f"[seed_full] Tournament player skip {uid}: {e}")

        # Seed match_players (derived from match pairs, not from mock data fields)
        for m in matches:
            match_id = m["id"]
            # Get actual match data from DB
            match_row = conn.execute(text("SELECT pair_a_id, pair_b_id FROM matches WHERE id = :id"), {"id": match_id}).mappings().first()
            if not match_row:
                continue
            for team, pair_id in [("A", match_row["pair_a_id"]), ("B", match_row["pair_b_id"])]:
                if not pair_id:
                    continue
                pair_row = conn.execute(text("SELECT player1_id, player2_id FROM pairs WHERE id = :id"), {"id": pair_id}).mappings().first()
                if not pair_row:
                    continue
                for idx, uid in enumerate([pair_row["player1_id"], pair_row["player2_id"]], 1):
                    if not uid:
                        continue
                    try:
                        conn.execute(text("""
                            INSERT INTO match_players (match_id, user_id, pair_id, team, player_number)
                            VALUES (:match_id, :user_id, :pair_id, :team, :player_number)
                            ON DUPLICATE KEY UPDATE team = VALUES(team)
                        """), {
                            "match_id": match_id,
                            "user_id": uid,
                            "pair_id": pair_id,
                            "team": team,
                            "player_number": idx,
                        })
                    except Exception as e:
                        print(f"[seed_full] Match player skip {uid}: {e}")

        # Seed match_events
        for m in matches:
            sets = m.get("sets", [])
            for set_idx, s in enumerate(sets, 1):
                try:
                    conn.execute(text("""
                        INSERT INTO match_events (id, match_id, set_number, game_number, event_type, description, winning_pair_id)
                        VALUES (:id, :match_id, :set_number, :game_number, 'SET_START', 'Inicio de set', NULL)
                        ON DUPLICATE KEY UPDATE event_type = VALUES(event_type)
                    """), {
                        "id": f"event_{m['id']}_set{set_idx}",
                        "match_id": m["id"],
                        "set_number": set_idx,
                        "game_number": 0,
                    })
                except Exception as e:
                    print(f"[seed_full] Match event skip {m['id']}: {e}")

        print("[seed_full] Full database seed completed successfully.")


if __name__ == "__main__":
    main()
