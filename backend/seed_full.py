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
        for user in users:
            role_name = user.get("role", "USER")
            role_id = role_map.get(role_name, role_map.get("USER"))
            if role_id:
                try:
                    conn.execute(text("""
                        INSERT INTO user_roles (user_id, role_id)
                        VALUES (:user_id, :role_id)
                        ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
                    """), {"user_id": user["id"], "role_id": role_id})
                except Exception as e:
                    print(f"[seed_full] User role skip {user['id']}: {e}")

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

        # Seed tournament_pairs
        for t in tournaments:
            cat_id = f"cat_{t['id']}"
            for pair in pairs:
                try:
                    conn.execute(text("""
                        INSERT INTO tournament_pairs (tournament_id, pair_id, category_id, seed, status)
                        VALUES (:tournament_id, :pair_id, :category_id, :seed, 'REGISTERED')
                        ON DUPLICATE KEY UPDATE status = VALUES(status)
                    """), {
                        "tournament_id": t["id"],
                        "pair_id": pair["id"],
                        "category_id": cat_id,
                        "seed": pair.get("seed"),
                    })
                except Exception as e:
                    print(f"[seed_full] Tournament pair skip {pair['id']}: {e}")

        # Seed tournament_players
        for t in tournaments:
            cat_id = f"cat_{t['id']}"
            for user in users:
                try:
                    conn.execute(text("""
                        INSERT INTO tournament_players (tournament_id, user_id, category_id, status)
                        VALUES (:tournament_id, :user_id, :category_id, 'REGISTERED')
                        ON DUPLICATE KEY UPDATE status = VALUES(status)
                    """), {
                        "tournament_id": t["id"],
                        "user_id": user["id"],
                        "category_id": cat_id,
                    })
                except Exception as e:
                    print(f"[seed_full] Tournament player skip {user['id']}: {e}")

        # Seed match_players
        for m in matches:
            team_a_players = [
                (m.get("player_a1_id"), "A", 1),
                (m.get("player_a2_id"), "A", 2),
            ]
            team_b_players = [
                (m.get("player_b1_id"), "B", 1),
                (m.get("player_b2_id"), "B", 2),
            ]
            for user_id, team, player_num in team_a_players + team_b_players:
                if not user_id:
                    continue
                try:
                    conn.execute(text("""
                        INSERT INTO match_players (match_id, user_id, pair_id, team, player_number)
                        VALUES (:match_id, :user_id, :pair_id, :team, :player_number)
                        ON DUPLICATE KEY UPDATE team = VALUES(team)
                    """), {
                        "match_id": m["id"],
                        "user_id": user_id,
                        "pair_id": m.get("pair_a_id") if team == "A" else m.get("pair_b_id"),
                        "team": team,
                        "player_number": player_num,
                    })
                except Exception as e:
                    print(f"[seed_full] Match player skip {user_id}: {e}")

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
