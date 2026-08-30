import json
import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Header, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
from database import init_db, engine, migrate_schema
from sqlalchemy import text
from jose import JWTError, jwt
import bcrypt

DEFAULT_STATS = {
    "pointsWon": 0, "winners": 0, "smashes": 0, "smashesWon": 0, "voleasWon": 0,
    "bandejas": 0, "viboras": 0, "remates": 0, "netPointsWon": 0, "touches": 0,
    "shots": 0, "serves": 0, "firstServes": 0, "secondServes": 0, "aces": 0,
    "doubleFaults": 0, "breakPoints": 0, "breakPointsWon": 0, "recoveries": 0,
    "globos": 0, "devoluciones": 0, "movesCount": 0, "matchesPlayed": 0,
    "matchesWon": 0, "matchesLost": 0, "setsWon": 0, "setsLost": 0, "gamesWon": 0,
    "gamesLost": 0, "pointsWon": 0, "netPointsWon": 0, "timePlayedMin": 0,
    "avgSpeedKmh": 0, "distanceKm": 0,
}

import re

_CAMEL_TO_SNAKE_MATCH = {
    "tournamentId": "tournament_id",
    "tournamentName": "tournament_name",
    "courtId": "court_id",
    "courtName": "court_name",
    "dateTime": "date_time",
    "pairAId": "pair_a_id",
    "pairBId": "pair_b_id",
    "pairAName": "pair_a_name",
    "pairBName": "pair_b_name",
    "playerA1Id": "player_a1_id",
    "playerA2Id": "player_a2_id",
    "playerB1Id": "player_b1_id",
    "playerB2Id": "player_b2_id",
    "playerA1Name": "player_a1_name",
    "playerA2Name": "player_a2_name",
    "playerB1Name": "player_b1_name",
    "playerB2Name": "player_b2_name",
    "playerA1Avatar": "player_a1_avatar",
    "playerA2Avatar": "player_a2_avatar",
    "playerB1Avatar": "player_b1_avatar",
    "playerB2Avatar": "player_b2_avatar",
    "currentGame": "current_game",
    "currentSetIndex": "current_set_index",
    "winnerPairId": "winner_pair_id",
    "winnerTeam": "winner_team",
    "startTimeMs": "start_time_ms",
    "elapsedTimeSec": "elapsed_time_sec",
    "goldenPoint": "golden_point",
    "setsToWin": "sets_to_win",
    "roundName": "round_name",
}

_CAMEL_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")

def _camel_to_snake(key: str) -> str:
    return _CAMEL_PATTERN.sub("_", key).lower()

def normalize_match_payload(match: dict) -> dict:
    out = {}
    for key, value in match.items():
        snake = _CAMEL_TO_SNAKE_MATCH.get(key)
        if snake is None:
            snake = _camel_to_snake(key)
        out[snake] = value
    return out

def normalize_stats(raw):
    if not raw:
        return dict(DEFAULT_STATS)
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = {}
    out = dict(DEFAULT_STATS)
    for k in out.keys():
        if k in raw and raw[k] is not None:
            out[k] = raw[k]
    return out

app = FastAPI(
    title="Padel Pro API",
    description="API REST para la gestión de torneos de padel",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://padel-pro-1-2nxt.onrender.com",
        "https://padel-pro-qj45.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "padel-pro-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = 7

def create_access_token(user_id: str, role: str):
    expire = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
    to_encode = {"sub": user_id, "role": role, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

_mock_data = None

def get_mock_data():
    global _mock_data
    if _mock_data is None:
        mock_path = os.path.join(os.path.dirname(__file__), "mock_data.json")
        with open(mock_path, "r", encoding="utf-8") as f:
            _mock_data = json.load(f)
    return _mock_data

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "Padel Pro API", "version": "1.0.0", "docs": "/docs"}

@app.get("/api")
def api_info():
    return {
        "service": "Padel Pro Backend",
        "version": "1.0.0",
        "endpoints": [
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/me",
            "/api/users",
            "/api/users/me",
            "/api/users/{user_id}",
            "/api/pairs",
            "/api/pairs/{pair_id}",
            "/api/tournaments",
            "/api/tournaments/{tournament_id}",
            "/api/courts",
            "/api/courts/{court_id}",
            "/api/matches",
            "/api/matches/{match_id}",
            "/api/audit-logs",
            "/api/notifications",
            "/api/stats",
            "/api/health",
            "/api/admin/migrate",
        ],
    }


@app.get("/api/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ok",
        "db": db_ok,
        "service": "padel-pro-backend",
    }


# ==================== AUTH ====================

@app.post("/api/auth/register")
def register(body: dict = Body(...)):
    email = body.get("email")
    password = body.get("password")
    name = body.get("name")
    surname = body.get("surname")
    username = body.get("username")
    role = body.get("role", "PLAYER")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    with engine.begin() as conn:
        result = conn.execute(text("SELECT user_id FROM users_auth WHERE email = :email"), {"email": email})
        if result.mappings().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        user_id = "usr_" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        conn.execute(text("""
            INSERT INTO users (id, name, surname, username, email, avatar, account_type, status, level, position, dominant_hand, points)
            VALUES (:id, :name, :surname, :username, :email, :avatar, 'USER', 'ACTIVE', :level, :position, :dominant_hand, :points)
        """), {
            "id": user_id,
            "name": name,
            "surname": surname,
            "username": username or email.split("@")[0],
            "email": email,
            "avatar": body.get("avatar"),
            "level": body.get("level"),
            "position": body.get("position"),
            "dominant_hand": body.get("dominant_hand"),
            "points": body.get("points", 0),
        })

        conn.execute(text("""
            INSERT INTO users_auth (user_id, email, hashed_password)
            VALUES (:user_id, :email, :hashed_password)
            ON DUPLICATE KEY UPDATE
                email = VALUES(email),
                hashed_password = VALUES(hashed_password)
        """), {
            "user_id": user_id,
            "email": email,
            "hashed_password": hashed,
        })

        role_row = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": role}).mappings().first()
        role_id = role_row["id"] if role_row else conn.execute(text("INSERT INTO roles (name) VALUES (:name)"), {"name": role}).lastrowid
        conn.execute(text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"), {"user_id": user_id, "role_id": role_id})

    token = create_access_token(user_id, role)
    return {"access_token": token, "token_type": "bearer", "user_id": user_id, "role": role}


@app.post("/api/auth/login")
def login(body: dict = Body(...)):
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users_auth WHERE email = :email"), {"email": email})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        auth_user = dict(row)
        if not bcrypt.checkpw(password.encode("utf-8"), auth_user["hashed_password"].encode("utf-8")):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = auth_user.get("user_id") or auth_user.get("id")
        role = auth_user.get("role")
        if role is None:
            role_row = conn.execute(text("""
                SELECT r.name FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id
                WHERE ur.user_id = :uid
                ORDER BY CASE r.name
                    WHEN 'SUPER_ADMIN' THEN 1
                    WHEN 'BUSINESS_ADMIN' THEN 2
                    WHEN 'BUSINESS_MANAGER' THEN 3
                    WHEN 'ADMIN' THEN 4
                    WHEN 'USER' THEN 5
                    ELSE 6
                END
                LIMIT 1
            """), {"uid": user_id}).mappings().first()
            role = role_row["name"] if role_row else "PLAYER"

        try:
            conn.execute(text("UPDATE users_auth SET last_login = :now WHERE user_id = :uid"),
                         {"now": datetime.utcnow(), "uid": user_id})
        except Exception:
            pass

        token = create_access_token(user_id, role)
        return {"access_token": token, "token_type": "bearer", "user_id": user_id, "role": role}


@app.get("/api/auth/me")
def auth_me(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT u.*, ua.email as auth_email,
                   (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
            FROM users u
            LEFT JOIN users_auth ua ON u.id = ua.user_id
            WHERE u.id = :id
        """), {"id": user_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        user = dict(row)
        return _build_user_response(user, user.get("role_name"))


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


ADMIN_ROLES = {"ADMIN", "SUPER_ADMIN", "BUSINESS_ADMIN", "BUSINESS_MANAGER"}

def require_admin(payload: dict = Depends(get_current_user)):
    if payload.get("role") not in ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload


@app.post("/api/admin/migrate")
def admin_migrate(payload: dict = Depends(require_admin)):
    try:
        with engine.begin() as conn:
            migrate_schema(conn)
        return {"status": "ok", "message": "Migration applied"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Migration failed: {e}")


def _build_user_response(user: dict, role_name: Optional[str] = None) -> dict:
    level = user.get("level") or "Intermedio"
    position = user.get("position") or "Drive (Derecha)"
    dominant_hand = user.get("dominant_hand") or "Derecha"
    stats = user.get("stats")
    if not stats:
        stats = {}
    return {
        "id": user.get("id"),
        "name": user.get("name") or "",
        "surname": user.get("surname") or "",
        "username": user.get("username") or "",
        "email": user.get("email") or "",
        "avatar": user.get("avatar") or "",
        "level": level,
        "position": position,
        "dominant_hand": dominant_hand,
        "points": user.get("points") or 0,
        "stats": stats,
        "role": role_name or "PLAYER",
        "account_type": user.get("account_type") or "USER",
        "status": user.get("status") or "ACTIVE",
        "invitation_code": user.get("invitation_code"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
        "phone": None,
        "current_pair_id": None,
        "partner_name": None,
    }


# ==================== USERS ====================

@app.get("/api/users")
def get_users():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT u.*, ua.email as auth_email,
                   (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
            FROM users u
            LEFT JOIN users_auth ua ON u.id = ua.user_id
            ORDER BY u.points DESC
        """))
        users = []
        for row in result.mappings():
            user = dict(row)
            users.append(_build_user_response(user, user.get("role_name")))
        return users


@app.get("/api/users/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    if authorization:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                with engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT u.*, ua.email as auth_email,
                               (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
                        FROM users u
                        LEFT JOIN users_auth ua ON u.id = ua.user_id
                        WHERE u.id = :id
                    """), {"id": user_id})
                    row = result.mappings().first()
                    if row:
                        user = dict(row)
                        return _build_user_response(user, user.get("role_name"))
    data = get_mock_data()
    return data["initial_user"]


@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT u.*, ua.email as auth_email,
                   (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
            FROM users u
            LEFT JOIN users_auth ua ON u.id = ua.user_id
            WHERE u.id = :id
        """), {"id": user_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        user = dict(row)
        return _build_user_response(user, user.get("role_name"))


@app.post("/api/users")
def create_user(user: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO users (id, name, surname, username, email, avatar, account_type, status, level, position, dominant_hand, points)
            VALUES (:id, :name, :surname, :username, :email, :avatar, 'USER', 'ACTIVE', :level, :position, :dominant_hand, :points)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), surname = VALUES(surname), username = VALUES(username),
                email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level),
                position = VALUES(position), dominant_hand = VALUES(dominant_hand),
                points = VALUES(points)
        """), {
            "id": user["id"],
            "name": user["name"],
            "surname": user.get("surname", ""),
            "username": user["username"],
            "email": user.get("email"),
            "avatar": user.get("avatar"),
            "level": user.get("level"),
            "position": user.get("position"),
            "dominant_hand": user.get("dominant_hand"),
            "points": user.get("points", 0),
        })

        if user.get("email"):
            hashed = bcrypt.hashpw((user.get("password") or "password").encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            conn.execute(text("""
                INSERT INTO users_auth (user_id, email, hashed_password)
                VALUES (:user_id, :email, :hashed_password)
                ON DUPLICATE KEY UPDATE email = VALUES(email), hashed_password = VALUES(hashed_password)
            """), {
                "user_id": user["id"],
                "email": user["email"],
                "hashed_password": hashed,
            })

        if user.get("role"):
            role_row = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": user["role"]}).mappings().first()
            role_id = role_row["id"] if role_row else conn.execute(text("INSERT INTO roles (name) VALUES (:name)"), {"name": user["role"]}).lastrowid
            conn.execute(text("""
                INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)
                ON DUPLICATE KEY UPDATE role_id = VALUES(role_id)
            """), {"user_id": user["id"], "role_id": role_id})

    return user


@app.put("/api/users/{user_id}")
def update_user(user_id: str, user: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="User not found")

        conn.execute(text("""
            UPDATE users SET name = :name, surname = :surname, username = :username,
                email = :email, avatar = :avatar, level = :level,
                position = :position, dominant_hand = :dominant_hand,
                points = :points
            WHERE id = :id
        """), {
            "id": user_id, "name": user["name"], "surname": user.get("surname", ""),
            "username": user["username"], "email": user.get("email"),
            "avatar": user.get("avatar"), "level": user.get("level"),
            "position": user.get("position"), "dominant_hand": user.get("dominant_hand"),
            "points": user.get("points", 0),
        })
    return {**user, "id": user_id}


@app.delete("/api/users/{user_id}")
def delete_user(user_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="User not found")
        conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
    return {"message": "User deleted"}

# ==================== PAIRS ====================

@app.get("/api/pairs")
def get_pairs():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM pairs ORDER BY created_at"))
        pairs = [dict(row) for row in result.mappings()]
        return pairs


@app.get("/api/pairs/{pair_id}")
def get_pair(pair_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM pairs WHERE id = :id"), {"id": pair_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Pair not found")
        return dict(row)


@app.post("/api/pairs")
def create_pair(pair: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO pairs (id, name, player1_id, player2_id, created_by, status, tournaments_disputed, titles_won)
            VALUES (:id, :name, :player1_id, :player2_id, :created_by, :status, :tournaments_disputed, :titles_won)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id),
                created_by = VALUES(created_by), status = VALUES(status),
                tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won)
        """), {
            "id": pair.get("id") or pair.get("player1Id") + "_" + pair.get("player2Id"),
            "name": pair.get("name"),
            "player1_id": pair.get("player1Id") or pair.get("player1_id"),
            "player2_id": pair.get("player2Id") or pair.get("player2_id"),
            "created_by": pair.get("createdBy") or pair.get("created_by") or pair.get("player1Id") or pair.get("player1_id"),
            "status": pair.get("status", "ACTIVE"),
            "tournaments_disputed": pair.get("tournamentsDisputed") or pair.get("tournaments_disputed"),
            "titles_won": pair.get("titlesWon") or pair.get("titles_won"),
        })
    return pair


@app.delete("/api/pairs/{pair_id}")
def delete_pair(pair_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM pairs WHERE id = :id"), {"id": pair_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Pair not found")
        conn.execute(text("DELETE FROM pairs WHERE id = :id"), {"id": pair_id})
    return {"message": "Pair deleted"}

# ==================== TOURNAMENTS ====================

def _build_tournament_response(t: dict) -> dict:
    rules = t.get("rules")
    if isinstance(rules, str):
        try:
            rules = json.loads(rules)
        except Exception:
            rules = {}
    if not rules or not isinstance(rules, dict):
        rules = {}
    if "pointsDistribution" not in rules or not isinstance(rules.get("pointsDistribution"), dict):
        rules["pointsDistribution"] = {
            "champion": 1000,
            "runnerUp": 600,
            "semiFinals": 360,
            "quarterFinals": 180,
            "groupStage": 90,
        }
    if "goldenPoint" not in rules:
        rules["goldenPoint"] = False
    if "tieBreakAt" not in rules:
        rules["tieBreakAt"] = 6
    if "finalSetTieBreak" not in rules:
        rules["finalSetTieBreak"] = False
    if "setsToWin" not in rules:
        rules["setsToWin"] = 2
    return {
        "id": t.get("id"),
        "name": t.get("name") or "",
        "logo": t.get("logo") or "🏆",
        "description": t.get("description") or "",
        "category": t.get("category") or "Masculino",
        "level": t.get("level") or "Intermedio",
        "location": t.get("location") or "",
        "start_date": t.get("start_date"),
        "end_date": t.get("end_date"),
        "status": t.get("status") or "DRAFT",
        "format": t.get("format") or "Eliminación directa",
        "max_pairs": t.get("max_pairs") or 0,
        "visibility": t.get("visibility") or "PRIVATE",
        "rules": rules,
        "registered_pair_ids": t.get("registered_pair_ids", []),
        "registered_user_ids": t.get("registered_user_ids", []),
        "court_ids": t.get("court_ids", []),
        "business_id": t.get("business_id"),
        "created_by": t.get("created_by"),
        "created_at": t.get("created_at"),
        "updated_at": t.get("updated_at"),
        "deleted_at": t.get("deleted_at"),
    }


@app.get("/api/tournaments")
def get_tournaments():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tournaments ORDER BY start_date"))
        tournaments = []
        for row in result.mappings():
            t = dict(row)
            t["registered_pair_ids"] = [r["pair_id"] for r in conn.execute(text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"), {"tid": t["id"]}).mappings()]
            t["registered_user_ids"] = [r["user_id"] for r in conn.execute(text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"), {"tid": t["id"]}).mappings()]
            tournaments.append(_build_tournament_response(t))
        return tournaments


@app.get("/api/tournaments/{tournament_id}")
def get_tournament(tournament_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Tournament not found")
        t = dict(row)
        t["registered_pair_ids"] = [r["pair_id"] for r in conn.execute(text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
        t["registered_user_ids"] = [r["user_id"] for r in conn.execute(text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
        return _build_tournament_response(t)


@app.post("/api/tournaments")
def create_tournament(tournament: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
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
            "id": tournament["id"], "business_id": tournament.get("business_id"),
            "created_by": tournament.get("created_by"), "name": tournament["name"],
            "logo": tournament.get("logo"), "description": tournament.get("description"),
            "category": tournament.get("category"), "level": tournament.get("level"),
            "location": tournament.get("location"), "start_date": tournament.get("start_date"),
            "end_date": tournament.get("end_date"), "status": tournament.get("status", "DRAFT"),
            "format": tournament.get("format"), "max_pairs": tournament.get("max_pairs"),
            "visibility": tournament.get("visibility", "PRIVATE"),
            "rules": json.dumps(tournament.get("rules", {})),
        })
    return tournament


@app.put("/api/tournaments/{tournament_id}")
def update_tournament(tournament_id: str, tournament: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Tournament not found")
        conn.execute(text("""
            UPDATE tournaments SET
                name = :name, logo = :logo, description = :description, category = :category,
                level = :level, location = :location, start_date = :start_date, end_date = :end_date,
                status = :status, format = :format, max_pairs = :max_pairs,
                visibility = :visibility, rules = :rules
            WHERE id = :id
        """), {
            "id": tournament_id,
            "name": tournament.get("name"), "logo": tournament.get("logo"),
            "description": tournament.get("description"), "category": tournament.get("category"),
            "level": tournament.get("level"), "location": tournament.get("location"),
            "start_date": tournament.get("start_date"), "end_date": tournament.get("end_date"),
            "status": tournament.get("status"), "format": tournament.get("format"),
            "max_pairs": tournament.get("max_pairs"),
            "visibility": tournament.get("visibility", "PRIVATE"),
            "rules": json.dumps(tournament.get("rules", {})),
        })
    return {**tournament, "id": tournament_id}


@app.post("/api/tournaments/{tournament_id}/register_user")
def register_user(tournament_id: str, body: dict, payload: dict = Depends(require_admin)):
    user_id = body.get("user_id")
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Tournament not found")
        conn.execute(text("""
            INSERT INTO tournament_players (tournament_id, user_id, status) VALUES (:tid, :uid, 'REGISTERED')
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """), {"tid": tournament_id, "uid": user_id})
    registered = [r["user_id"] for r in conn.execute(text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
    return {"message": "User registered", "registered_user_ids": registered}


@app.post("/api/tournaments/{tournament_id}/register")
def register_pair(tournament_id: str, body: dict, payload: dict = Depends(require_admin)):
    pair_id = body.get("pair_id")
    court_id = body.get("court_id")
    date_time = body.get("date_time")
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Tournament not found")
        conn.execute(text("""
            INSERT INTO tournament_pairs (tournament_id, pair_id, status) VALUES (:tid, :pid, 'REGISTERED')
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """), {"tid": tournament_id, "pid": pair_id})
    registered = [r["pair_id"] for r in conn.execute(text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
    return {"message": "Pair registered", "registered_pair_ids": registered, "court_ids": []}


@app.delete("/api/tournaments/{tournament_id}")
def delete_tournament(tournament_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Tournament not found")
        conn.execute(text("DELETE FROM matches WHERE tournament_id = :tid"), {"tid": tournament_id})
        conn.execute(text("DELETE FROM tournaments WHERE id = :tid"), {"tid": tournament_id})
    return {"message": "Tournament deleted"}

# ==================== COURTS ====================

@app.get("/api/courts")
def get_courts():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courts ORDER BY number"))
        courts = [dict(row) for row in result.mappings()]
        return courts

@app.get("/api/courts/{court_id}")
def get_court(court_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courts WHERE id = :id"), {"id": court_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Court not found")
        return dict(row)

@app.put("/api/courts/{court_id}")
def update_court(court_id: str, court: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM courts WHERE id = :id"), {"id": court_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Court not found")
        conn.execute(text("""
            UPDATE courts SET name = :name, location = :location, number = :number,
                status = :status
            WHERE id = :id
        """), {
            "id": court_id, "name": court["name"], "location": court.get("location"),
            "number": court.get("number"), "status": court["status"],
        })
    return {**court, "id": court_id}

# ==================== MATCHES ====================

@app.get("/api/matches")
def get_matches():
    with engine.connect() as conn:
        try:
            result = conn.execute(text("""
                SELECT m.id,
                    m.tournament_id AS tournamentId,
                    m.round_id AS roundId,
                    m.business_id AS businessId,
                    m.court_id AS courtId,
                    m.created_by AS createdBy,
                    m.pair_a_id AS pairAId,
                    m.pair_b_id AS pairBId,
                    m.date_time AS dateTime,
                    m.status,
                    m.visibility,
                    m.sets,
                    m.current_set_index AS currentSetIndex,
                    m.winner_pair_id AS winnerPairId,
                    m.winner_team AS winnerTeam,
                    m.start_time_ms AS startTimeMs,
                    m.elapsed_time_sec AS elapsedTimeSec,
                    m.golden_point AS goldenPoint,
                    m.sets_to_win AS setsToWin,
                    m.round_name AS roundName,
                    m.created_at AS createdAt,
                    m.updated_at AS updatedAt,
                    m.deleted_at AS deletedAt,
                    t.name AS tournamentName,
                    c.name AS courtName,
                    pa.name AS pairAName,
                    pb.name AS pairBName,
                    ua1.name AS playerA1Name,
                    ua2.name AS playerA2Name,
                    ub1.name AS playerB1Name,
                    ub2.name AS playerB2Name,
                    ua1.avatar AS playerA1Avatar,
                    ua2.avatar AS playerA2Avatar,
                    ub1.avatar AS playerB1Avatar,
                    ub2.avatar AS playerB2Avatar
                FROM matches m
                LEFT JOIN tournaments t ON m.tournament_id = t.id
                LEFT JOIN courts c ON m.court_id = c.id
                LEFT JOIN pairs pa ON m.pair_a_id = pa.id
                LEFT JOIN pairs pb ON m.pair_b_id = pb.id
                LEFT JOIN users ua1 ON m.player_a1_id = ua1.id
                LEFT JOIN users ua2 ON m.player_a2_id = ua2.id
                LEFT JOIN users ub1 ON m.player_b1_id = ub1.id
                LEFT JOIN users ub2 ON m.player_b2_id = ub2.id
                ORDER BY m.date_time
            """))
        except Exception:
            result = conn.execute(text("""
                SELECT m.id,
                    m.tournament_id AS tournamentId,
                    m.court_id AS courtId,
                    m.created_by AS createdBy,
                    m.pair_a_id AS pairAId,
                    m.pair_b_id AS pairBId,
                    m.date_time AS dateTime,
                    m.status,
                    m.sets,
                    m.created_at AS createdAt,
                    m.updated_at AS updatedAt,
                    t.name AS tournamentName,
                    c.name AS courtName,
                    pa.name AS pairAName,
                    pb.name AS pairBName,
                    ua1.name AS playerA1Name,
                    ua2.name AS playerA2Name,
                    ub1.name AS playerB1Name,
                    ub2.name AS playerB2Name,
                    ua1.avatar AS playerA1Avatar,
                    ua2.avatar AS playerA2Avatar,
                    ub1.avatar AS playerB1Avatar,
                    ub2.avatar AS playerB2Avatar
                FROM matches m
                LEFT JOIN tournaments t ON m.tournament_id = t.id
                LEFT JOIN courts c ON m.court_id = c.id
                LEFT JOIN pairs pa ON m.pair_a_id = pa.id
                LEFT JOIN pairs pb ON m.pair_b_id = pb.id
                LEFT JOIN users ua1 ON m.player_a1_id = ua1.id
                LEFT JOIN users ua2 ON m.player_a2_id = ua2.id
                LEFT JOIN users ub1 ON m.player_b1_id = ub1.id
                LEFT JOIN users ub2 ON m.player_b2_id = ub2.id
                ORDER BY m.date_time
            """))
        matches = []
        for row in result.mappings():
            m = dict(row)
            if isinstance(m.get("sets"), str):
                m["sets"] = json.loads(m["sets"])
            m.setdefault("roundId", None)
            m.setdefault("businessId", None)
            m.setdefault("visibility", "PRIVATE")
            m.setdefault("currentSetIndex", 0)
            m.setdefault("winnerPairId", None)
            m.setdefault("winnerTeam", None)
            m.setdefault("startTimeMs", None)
            m.setdefault("elapsedTimeSec", 0)
            m.setdefault("goldenPoint", 0)
            m.setdefault("setsToWin", 2)
            m.setdefault("roundName", None)
            m.setdefault("deletedAt", None)
            m.setdefault("playerA1Name", m.get("playerA1Name") or "Jugador 1")
            m.setdefault("playerA2Name", m.get("playerA2Name") or "Jugador 2")
            m.setdefault("playerB1Name", m.get("playerB1Name") or "Jugador 3")
            m.setdefault("playerB2Name", m.get("playerB2Name") or "Jugador 4")
            m.setdefault("playerA1Avatar", m.get("playerA1Avatar") or "")
            m.setdefault("playerA2Avatar", m.get("playerA2Avatar") or "")
            m.setdefault("playerB1Avatar", m.get("playerB1Avatar") or "")
            m.setdefault("playerB2Avatar", m.get("playerB2Avatar") or "")
            m.setdefault("pairAName", m.get("pairAName") or "Pareja A")
            m.setdefault("pairBName", m.get("pairBName") or "Pareja B")
            m.setdefault("courtName", m.get("courtName") or "Pista por definir")
            m["current_game"] = {}
            matches.append(m)
        return matches


@app.get("/api/matches/{match_id}")
def get_match(match_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT m.id,
                m.tournament_id AS tournamentId,
                m.round_id AS roundId,
                m.business_id AS businessId,
                m.court_id AS courtId,
                m.created_by AS createdBy,
                m.pair_a_id AS pairAId,
                m.pair_b_id AS pairBId,
                m.date_time AS dateTime,
                m.status,
                m.visibility,
                m.sets,
                m.current_set_index AS currentSetIndex,
                m.winner_pair_id AS winnerPairId,
                m.winner_team AS winnerTeam,
                m.start_time_ms AS startTimeMs,
                m.elapsed_time_sec AS elapsedTimeSec,
                m.golden_point AS goldenPoint,
                m.sets_to_win AS setsToWin,
                m.round_name AS roundName,
                m.created_at AS createdAt,
                m.updated_at AS updatedAt,
                m.deleted_at AS deletedAt,
                t.name AS tournamentName,
                c.name AS courtName,
                pa.name AS pairAName,
                pb.name AS pairBName,
                ua1.name AS playerA1Name,
                ua2.name AS playerA2Name,
                ub1.name AS playerB1Name,
                ub2.name AS playerB2Name,
                ua1.avatar AS playerA1Avatar,
                ua2.avatar AS playerA2Avatar,
                ub1.avatar AS playerB1Avatar,
                ub2.avatar AS playerB2Avatar
            FROM matches m
            LEFT JOIN tournaments t ON m.tournament_id = t.id
            LEFT JOIN courts c ON m.court_id = c.id
            LEFT JOIN pairs pa ON m.pair_a_id = pa.id
            LEFT JOIN pairs pb ON m.pair_b_id = pb.id
            LEFT JOIN users ua1 ON m.player_a1_id = ua1.id
            LEFT JOIN users ua2 ON m.player_a2_id = ua2.id
            LEFT JOIN users ub1 ON m.player_b1_id = ub1.id
            LEFT JOIN users ub2 ON m.player_b2_id = ub2.id
            WHERE m.id = :id
        """), {"id": match_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Match not found")
        m = dict(row)
        if isinstance(m.get("sets"), str):
            m["sets"] = json.loads(m["sets"])
        m["current_game"] = {}
        return m


@app.post("/api/matches")
def create_match(match: dict, payload: dict = Depends(require_admin)):
    match = normalize_match_payload(match)
    with engine.begin() as conn:
        pair_a_id = match.get("pair_a_id")
        pair_b_id = match.get("pair_b_id")
        if pair_a_id and not match.get("player_a1_id"):
            row = conn.execute(text("SELECT * FROM pairs WHERE id = :id"), {"id": pair_a_id}).mappings().first()
            if row:
                match["player_a1_id"] = row.get("player1_id")
                match["player_a2_id"] = row.get("player2_id")
        if pair_b_id and not match.get("player_b1_id"):
            row = conn.execute(text("SELECT * FROM pairs WHERE id = :id"), {"id": pair_b_id}).mappings().first()
            if row:
                match["player_b1_id"] = row.get("player1_id")
                match["player_b2_id"] = row.get("player2_id")

        conn.execute(text("""
            INSERT INTO matches (id, tournament_id, round_id, business_id, court_id, created_by,
                pair_a_id, pair_b_id, date_time, status, visibility, sets, current_set_index,
                winner_pair_id, winner_team, start_time_ms, elapsed_time_sec, golden_point,
                sets_to_win, round_name)
            VALUES (:id, :tournament_id, :round_id, :business_id, :court_id, :created_by,
                :pair_a_id, :pair_b_id, :date_time, :status, :visibility, :sets, :current_set_index,
                :winner_pair_id, :winner_team, :start_time_ms, :elapsed_time_sec, :golden_point,
                :sets_to_win, :round_name)
        """), {
            "id": match["id"], "tournament_id": match.get("tournament_id"),
            "round_id": match.get("round_id"), "business_id": match.get("business_id"),
            "court_id": match.get("court_id"), "created_by": match.get("created_by"),
            "pair_a_id": match.get("pair_a_id"), "pair_b_id": match.get("pair_b_id"),
            "date_time": match.get("date_time"), "status": match.get("status", "SCHEDULED"),
            "visibility": match.get("visibility", "PRIVATE"),
            "sets": json.dumps(match.get("sets", [])),
            "current_set_index": match.get("current_set_index", 0),
            "winner_pair_id": match.get("winner_pair_id"), "winner_team": match.get("winner_team"),
            "start_time_ms": match.get("start_time_ms"), "elapsed_time_sec": match.get("elapsed_time_sec", 0),
            "golden_point": 1 if match.get("golden_point") else 0,
            "sets_to_win": match.get("sets_to_win", 2),
            "round_name": match.get("round_name"),
        })
    return match


@app.put("/api/matches/{match_id}")
def update_match(match_id: str, match: dict, payload: dict = Depends(get_current_user)):
    match = normalize_match_payload(match)
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Match not found")
        conn.execute(text("""
            UPDATE matches SET tournament_id = :tournament_id, round_id = :round_id,
                business_id = :business_id, court_id = :court_id, created_by = :created_by,
                pair_a_id = :pair_a_id, pair_b_id = :pair_b_id, date_time = :date_time,
                status = :status, visibility = :visibility, sets = :sets, current_set_index = :current_set_index,
                winner_pair_id = :winner_pair_id, winner_team = :winner_team,
                start_time_ms = :start_time_ms, elapsed_time_sec = :elapsed_time_sec,
                golden_point = :golden_point, sets_to_win = :sets_to_win, round_name = :round_name
            WHERE id = :id
        """), {
            "id": match_id,
            "tournament_id": match.get("tournament_id"), "round_id": match.get("round_id"),
            "business_id": match.get("business_id"), "court_id": match.get("court_id"),
            "created_by": match.get("created_by"), "pair_a_id": match.get("pair_a_id"),
            "pair_b_id": match.get("pair_b_id"), "date_time": match.get("date_time"),
            "status": match.get("status"), "visibility": match.get("visibility"),
            "sets": json.dumps(match.get("sets", [])),
            "current_set_index": match.get("current_set_index", 0),
            "winner_pair_id": match.get("winner_pair_id"), "winner_team": match.get("winner_team"),
            "start_time_ms": match.get("start_time_ms"), "elapsed_time_sec": match.get("elapsed_time_sec", 0),
            "golden_point": 1 if match.get("golden_point") else 0,
            "sets_to_win": match.get("sets_to_win", 2),
            "round_name": match.get("round_name"),
        })
    return {**match, "id": match_id}


@app.put("/api/matches/{match_id}/court")
def update_match_court(match_id: str, body: dict, payload: dict = Depends(require_admin)):
    court_id = body.get("court_id")
    court_name = body.get("court_name")
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Match not found")
        conn.execute(text("UPDATE matches SET court_id = :cid WHERE id = :id"),
                     {"cid": court_id, "id": match_id})
    return {"message": "Court updated", "court_id": court_id, "court_name": court_name}


@app.delete("/api/matches/{match_id}")
def delete_match(match_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Match not found")
        conn.execute(text("DELETE FROM matches WHERE id = :id"), {"id": match_id})
    return {"message": "Match deleted", "match_id": match_id}


@app.post("/api/matches/{match_id}/finish")
def finish_match(match_id: str, body: dict, payload: dict = Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Match not found")
        match = dict(row)
        if isinstance(match.get("sets"), str):
            match["sets"] = json.loads(match["sets"])

        winner_team = body.get("winner_team") or match.get("winner_team")
        if not winner_team:
            sets = match.get("sets", [])
            a_wins = sum(1 for s in sets if s.get("winner") == "A")
            b_wins = sum(1 for s in sets if s.get("winner") == "B")
            winner_team = "A" if a_wins >= b_wins else "B"
        is_winner_a = str(winner_team).upper() == "A"

        player_a1_id = match.get("player_a1_id")
        player_a2_id = match.get("player_a2_id")
        player_b1_id = match.get("player_b1_id")
        player_b2_id = match.get("player_b2_id")

        if not player_a1_id or not player_a2_id or not player_b1_id or not player_b2_id:
            pair_a_id = match.get("pair_a_id")
            pair_b_id = match.get("pair_b_id")
            if pair_a_id:
                pair_a = conn.execute(text("SELECT * FROM pairs WHERE id = :id"), {"id": pair_a_id}).mappings().first()
                if pair_a:
                    pair_a = dict(pair_a)
                    if not player_a1_id:
                        player_a1_id = pair_a.get("player1_id")
                    if not player_a2_id:
                        player_a2_id = pair_a.get("player2_id")
            if pair_b_id:
                pair_b = conn.execute(text("SELECT * FROM pairs WHERE id = :id"), {"id": pair_b_id}).mappings().first()
                if pair_b:
                    pair_b = dict(pair_b)
                    if not player_b1_id:
                        player_b1_id = pair_b.get("player1_id")
                    if not player_b2_id:
                        player_b2_id = pair_b.get("player2_id")

        if is_winner_a:
            winner_player_ids = [player_a1_id, player_a2_id]
            loser_player_ids = [player_b1_id, player_b2_id]
        else:
            winner_player_ids = [player_b1_id, player_b2_id]
            loser_player_ids = [player_a1_id, player_a2_id]

        conn.execute(text("""
            UPDATE matches SET status = 'FINISHED', winner_team = :winner_team
            WHERE id = :id
        """), {
            "id": match_id,
            "winner_team": winner_team,
        })

        def update_player_points(user_id: str, won: bool):
            if not user_id:
                return
            sets = match.get("sets", [])
            if won:
                player_winner = "A" if is_winner_a else "B"
                base_points = 150
            else:
                player_winner = "B" if is_winner_a else "A"
                base_points = 30
            sets_won = sum(1 for s in sets if s.get("winner") == player_winner)
            conn.execute(text("""
                INSERT INTO user_points (user_id, match_id, points, reason)
                VALUES (:uid, :mid, :pts, :reason)
            """), {
                "uid": user_id, "mid": match_id, "pts": base_points,
                "reason": "match_finish_winner" if won else "match_finish_loser"
            })
            conn.execute(text("""
                UPDATE users SET points = points + :pts WHERE id = :uid
            """), {"pts": base_points, "uid": user_id})

        for pid in winner_player_ids:
            update_player_points(pid, True)
        for pid in loser_player_ids:
            update_player_points(pid, False)

    if body.get("create_notification") and body.get("notification"):
        notif = body["notification"]
        try:
            api.create_notification(notif)
        except Exception:
            pass
    return {"message": "Match finished", "match_id": match_id, "winner_team": winner_team}


@app.post("/api/matches/{match_id}/events")
def create_match_event(match_id: str, event: dict, payload: dict = Depends(get_current_user)):
    event = normalize_match_payload(event)
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO match_events (id, match_id, set_number, game_number, timestamp,
                winning_pair_id, player_id, event_type, description, score_snapshot)
            VALUES (:id, :match_id, :set_number, :game_number, :timestamp,
                :winning_pair_id, :player_id, :event_type, :description, :score_snapshot)
        """), {
            "id": event["id"],
            "match_id": match_id,
            "set_number": event.get("set_number", 0),
            "game_number": event.get("game_number", 0),
            "timestamp": event.get("timestamp", ""),
            "winning_pair_id": event.get("winning_pair_id"),
            "player_id": event.get("player_id"),
            "event_type": event.get("event_type", "POINT"),
            "description": event.get("description"),
            "score_snapshot": event.get("score_snapshot"),
        })
    return event

# ==================== AUDIT LOGS ====================

@app.get("/api/audit-logs")
def get_audit_logs(payload: dict = Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM audit_logs ORDER BY timestamp DESC"))
        logs = [dict(row) for row in result.mappings()]
        return logs


@app.post("/api/audit-logs")
def create_audit_log(log: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO audit_logs (id, business_id, user_id, action, target_type, target_id, details, timestamp)
            VALUES (:id, :business_id, :user_id, :action, :target_type, :target_id, :details, :timestamp)
            ON DUPLICATE KEY UPDATE
                business_id = VALUES(business_id), user_id = VALUES(user_id),
                action = VALUES(action), target_type = VALUES(target_type),
                target_id = VALUES(target_id), details = VALUES(details), timestamp = VALUES(timestamp)
        """), {
            "id": log["id"], "business_id": log.get("business_id"), "user_id": log.get("user_id"),
            "action": log["action"], "target_type": log.get("target_type", "unknown"),
            "target_id": log.get("target_id", ""), "details": json.dumps(log.get("details", {})),
            "timestamp": log["timestamp"],
        })
    return log

# ==================== NOTIFICATIONS ====================

@app.get("/api/notifications")
def get_notifications(payload: dict = Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM notifications ORDER BY timestamp DESC"))
        notifs = [dict(row) for row in result.mappings()]
        return notifs


@app.post("/api/notifications")
def create_notification(notification: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO notifications (id, user_id, title, body, timestamp, read_status, type, link_id)
            VALUES (:id, :user_id, :title, :body, :timestamp, :read_status, :type, :link_id)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title), body = VALUES(body), read_status = VALUES(read_status),
                type = VALUES(type), link_id = VALUES(link_id)
        """), {
            "id": notification["id"], "user_id": notification.get("user_id"),
            "title": notification["title"], "body": notification.get("body"),
            "timestamp": notification["timestamp"], "read_status": 1 if notification.get("read") else 0,
            "type": notification.get("type"), "link_id": notification.get("link_id"),
        })
    return notification

# ==================== STATS ====================

@app.get("/api/stats")
def get_stats():
    with engine.connect() as conn:
        total_matches = conn.execute(text("SELECT COUNT(*) FROM matches")).scalar()
        total_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments")).scalar()
        total_players = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
        total_pairs = conn.execute(text("SELECT COUNT(*) FROM pairs")).scalar()
        total_courts = conn.execute(text("SELECT COUNT(*) FROM courts")).scalar()
        total_notifications = conn.execute(text("SELECT COUNT(*) FROM notifications")).scalar()
        total_audit_logs = conn.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar()

        live_matches = conn.execute(text("SELECT COUNT(*) FROM matches WHERE status = 'IN_PROGRESS'")).scalar()
        upcoming_matches = conn.execute(text("SELECT COUNT(*) FROM matches WHERE status = 'SCHEDULED'")).scalar()
        finished_matches = conn.execute(text("SELECT COUNT(*) FROM matches WHERE status = 'FINISHED'")).scalar()

        active_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments WHERE status = 'IN_PROGRESS'")).scalar()
        open_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments WHERE status = 'OPEN'")).scalar()
        draft_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments WHERE status = 'DRAFT'")).scalar()

        return {
            "total_players": total_players,
            "total_pairs": total_pairs,
            "total_courts": total_courts,
            "total_tournaments": total_tournaments,
            "total_matches": total_matches,
            "total_audit_logs": total_audit_logs,
            "total_notifications": total_notifications,
            "matches_by_status": {
                "live": live_matches,
                "upcoming": upcoming_matches,
                "finished": finished_matches
            },
            "tournaments_by_status": {
                "active": active_tournaments,
                "open": open_tournaments,
                "draft": draft_tournaments
            }
        }

# ==================== DB DIRECT QUERIES ====================

@app.get("/api/db/users")
def db_get_users(payload: dict = Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT u.*, ua.email as auth_email,
                   (SELECT r.name FROM user_roles ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id = u.id LIMIT 1) as role_name
            FROM users u
            LEFT JOIN users_auth ua ON u.id = ua.user_id
            ORDER BY u.points DESC
        """))
        users = []
        for row in result.mappings():
            user = dict(row)
            users.append(_build_user_response(user, user.get("role_name")))
        return users


@app.get("/api/db/matches")
def db_get_matches(payload: dict = Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM matches ORDER BY date_time"))
        matches = []
        for row in result.mappings():
            m = dict(row)
            if isinstance(m.get("sets"), str):
                m["sets"] = json.loads(m["sets"])
            matches.append(m)
        return matches
