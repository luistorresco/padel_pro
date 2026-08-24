import json
import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Header, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
from database import init_db, engine
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
    allow_origins=["*"],
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
    return {"service": "Padel Pro Backend", "version": "1.0.0", "endpoints": [
        "/api/auth/login", "/api/auth/register", "/api/auth/me",
        "/api/users", "/api/users/me", "/api/users/{user_id}",
        "/api/pairs", "/api/pairs/{pair_id}",
        "/api/tournaments", "/api/tournaments/{tournament_id}",
        "/api/courts", "/api/courts/{court_id}",
        "/api/matches", "/api/matches/{match_id}",
        "/api/audit-logs", "/api/notifications",
        "/api/gesture-config", "/api/stats"
    ]}

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
        result = conn.execute(text("SELECT * FROM users_auth WHERE email = :email"), {"email": email})
        if result.mappings().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        user_id = "usr_" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        conn.execute(text("""
            INSERT INTO users_auth (id, email, hashed_password, role)
            VALUES (:id, :email, :hashed_password, :role)
        """), {
            "id": user_id,
            "email": email,
            "hashed_password": hashed,
            "role": role,
        })

        if name and surname:
            conn.execute(text("""
                INSERT INTO users (id, name, surname, username, email, role, avatar, level,
                    position, dominant_hand, current_pair_id, points, partner_name, phone, stats)
                VALUES (:id, :name, :surname, :username, :email, :role, :avatar, :level,
                    :position, :dominant_hand, :current_pair_id, :points, :partner_name, :phone, :stats)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name, surname = EXCLUDED.surname, username = EXCLUDED.username,
                    email = EXCLUDED.email, role = EXCLUDED.role, avatar = EXCLUDED.avatar,
                    level = EXCLUDED.level, position = EXCLUDED.position,
                    dominant_hand = EXCLUDED.dominant_hand, current_pair_id = EXCLUDED.current_pair_id,
                    points = EXCLUDED.points, partner_name = EXCLUDED.partner_name,
                    phone = EXCLUDED.phone, stats = EXCLUDED.stats
            """), {
                "id": user_id,
                "name": name,
                "surname": surname,
                "username": username or email.split("@")[0],
                "email": email,
                "role": role,
                "avatar": body.get("avatar"),
                "level": body.get("level"),
                "position": body.get("position"),
                "dominant_hand": body.get("dominant_hand"),
                "current_pair_id": body.get("current_pair_id"),
                "points": body.get("points", 0),
                "partner_name": body.get("partner_name"),
                "phone": body.get("phone"),
                "stats": json.dumps(normalize_stats(body.get("stats"))),
            })

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

        token = create_access_token(auth_user["id"], auth_user["role"])
        return {"access_token": token, "token_type": "bearer", "user_id": auth_user["id"], "role": auth_user["role"]}


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
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        user = dict(row)
        if isinstance(user.get("stats"), str):
            user["stats"] = json.loads(user["stats"])
        return user


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


def require_admin(payload: dict = Depends(get_current_user)):
    if payload.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

# ==================== USERS ====================

@app.get("/api/users")
def get_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users ORDER BY points DESC"))
        users = []
        for row in result.mappings():
            user = dict(row)
            if isinstance(user.get("stats"), str):
                user["stats"] = json.loads(user["stats"])
            if not user.get("stats"):
                user["stats"] = {}
            users.append(user)
        return users

@app.get("/api/users/me")
def get_current_user():
    data = get_mock_data()
    return data["initial_user"]

@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        user = dict(row)
        if isinstance(user.get("stats"), str):
            user["stats"] = json.loads(user["stats"])
        if not user.get("stats"):
            user["stats"] = {}
        return user

@app.post("/api/users")
def create_user(user: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO users (id, name, surname, username, email, role, avatar, level,
                position, dominant_hand, current_pair_id, points, partner_name, phone, stats)
            VALUES (:id, :name, :surname, :username, :email, :role, :avatar, :level,
                :position, :dominant_hand, :current_pair_id, :points, :partner_name, :phone, :stats)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name, surname = EXCLUDED.surname, username = EXCLUDED.username,
                email = EXCLUDED.email, role = EXCLUDED.role, avatar = EXCLUDED.avatar,
                level = EXCLUDED.level, position = EXCLUDED.position,
                dominant_hand = EXCLUDED.dominant_hand, current_pair_id = EXCLUDED.current_pair_id,
                points = EXCLUDED.points, partner_name = EXCLUDED.partner_name,
                phone = EXCLUDED.phone, stats = EXCLUDED.stats
        """), {
            "id": user["id"], "name": user["name"], "surname": user["surname"],
            "username": user["username"], "email": user["email"], "role": user["role"],
            "avatar": user.get("avatar"), "level": user.get("level"),
            "position": user.get("position"), "dominant_hand": user.get("dominant_hand"),
            "current_pair_id": user.get("current_pair_id"), "points": user.get("points", 0),
            "partner_name": user.get("partner_name"), "phone": user.get("phone"),
            "stats": json.dumps(normalize_stats(user.get("stats"))),
        })
    return user

@app.put("/api/users/{user_id}")
def update_user(user_id: str, user: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="User not found")
        
        conn.execute(text("""
            UPDATE users SET name = :name, surname = :surname, username = :username,
                email = :email, role = :role, avatar = :avatar, level = :level,
                position = :position, dominant_hand = :dominant_hand,
                current_pair_id = :current_pair_id, points = :points,
                partner_name = :partner_name, phone = :phone, stats = :stats
            WHERE id = :id
        """), {
            "id": user_id, "name": user["name"], "surname": user["surname"],
            "username": user["username"], "email": user["email"], "role": user["role"],
            "avatar": user.get("avatar"), "level": user.get("level"),
            "position": user.get("position"), "dominant_hand": user.get("dominant_hand"),
            "current_pair_id": user.get("current_pair_id"), "points": user.get("points", 0),
            "partner_name": user.get("partner_name"), "phone": user.get("phone"),
            "stats": json.dumps(user.get("stats", {})),
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
            INSERT INTO pairs (id, name, player1_id, player2_id, player1_name, player2_name,
                player1_avatar, player2_avatar, created_at, status, tournaments_disputed, titles_won)
            VALUES (:id, :name, :player1_id, :player2_id, :player1_name, :player2_name,
                :player1_avatar, :player2_avatar, :created_at, :status, :tournaments_disputed, :titles_won)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name, player1_id = EXCLUDED.player1_id, player2_id = EXCLUDED.player2_id,
                player1_name = EXCLUDED.player1_name, player2_name = EXCLUDED.player2_name,
                player1_avatar = EXCLUDED.player1_avatar, player2_avatar = EXCLUDED.player2_avatar,
                created_at = EXCLUDED.created_at, status = EXCLUDED.status,
                tournaments_disputed = EXCLUDED.tournaments_disputed, titles_won = EXCLUDED.titles_won
        """), {
            "id": pair.get("id") or pair.get("player1Id") + "_" + pair.get("player2Id"),
            "name": pair.get("name"),
            "player1_id": pair.get("player1Id") or pair.get("player1_id"),
            "player2_id": pair.get("player2Id") or pair.get("player2_id"),
            "player1_name": pair.get("player1Name") or pair.get("player1_name"),
            "player2_name": pair.get("player2Name") or pair.get("player2_name"),
            "player1_avatar": pair.get("player1Avatar") or pair.get("player1_avatar"),
            "player2_avatar": pair.get("player2Avatar") or pair.get("player2_avatar"),
            "created_at": pair.get("createdAt") or pair.get("created_at"),
            "status": pair.get("status"),
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

@app.get("/api/tournaments")
def get_tournaments():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tournaments ORDER BY start_date"))
        tournaments = []
        for row in result.mappings():
            t = dict(row)
            if isinstance(t.get("registered_pair_ids"), str):
                t["registered_pair_ids"] = json.loads(t["registered_pair_ids"])
            else:
                t["registered_pair_ids"] = []
            if isinstance(t.get("rules"), str):
                t["rules"] = json.loads(t["rules"])
            else:
                t["rules"] = {}
            if isinstance(t.get("court_ids"), str):
                t["court_ids"] = json.loads(t["court_ids"])
            else:
                t["court_ids"] = []
            tournaments.append(t)
        return tournaments

@app.get("/api/tournaments/{tournament_id}")
def get_tournament(tournament_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Tournament not found")
        t = dict(row)
        if isinstance(t.get("registered_pair_ids"), str):
            t["registered_pair_ids"] = json.loads(t["registered_pair_ids"])
        else:
            t["registered_pair_ids"] = []
        if isinstance(t.get("rules"), str):
            t["rules"] = json.loads(t["rules"])
        else:
            t["rules"] = {}
        if isinstance(t.get("court_ids"), str):
            t["court_ids"] = json.loads(t["court_ids"])
        else:
            t["court_ids"] = []
        return t

@app.post("/api/tournaments")
def create_tournament(tournament: dict, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO tournaments (id, name, logo, description, category, level, location,
                start_date, end_date, status, format, max_pairs, registered_pair_ids, rules, court_ids)
            VALUES (:id, :name, :logo, :description, :category, :level, :location,
                :start_date, :end_date, :status, :format, :max_pairs, :registered_pair_ids, :rules, :court_ids)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name, logo = EXCLUDED.logo, description = EXCLUDED.description,
                category = EXCLUDED.category, level = EXCLUDED.level, location = EXCLUDED.location,
                start_date = EXCLUDED.start_date, end_date = EXCLUDED.end_date, status = EXCLUDED.status,
                format = EXCLUDED.format, max_pairs = EXCLUDED.max_pairs,
                registered_pair_ids = EXCLUDED.registered_pair_ids, rules = EXCLUDED.rules, court_ids = EXCLUDED.court_ids
        """), {
            "id": tournament["id"], "name": tournament["name"], "logo": tournament.get("logo"),
            "description": tournament.get("description"), "category": tournament.get("category"),
            "level": tournament.get("level"), "location": tournament.get("location"),
            "start_date": tournament.get("start_date"), "end_date": tournament.get("end_date"),
            "status": tournament.get("status"), "format": tournament.get("format"),
            "max_pairs": tournament.get("max_pairs"),
            "registered_pair_ids": json.dumps(tournament.get("registered_pair_ids", [])),
            "rules": json.dumps(tournament.get("rules", {})),
            "court_ids": json.dumps(tournament.get("court_ids", [])),
        })
    return tournament

@app.delete("/api/tournaments/{tournament_id}")
def delete_tournament(tournament_id: str, payload: dict = Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Tournament not found")
        conn.execute(text("DELETE FROM matches WHERE tournament_id = :tid"), {"tid": tournament_id})
        conn.execute(text("DELETE FROM tournaments WHERE id = :tid"), {"tid": tournament_id})
    return {"message": "Tournament deleted"}

@app.post("/api/tournaments/{tournament_id}/register")
def register_pair(tournament_id: str, body: dict, payload: dict = Depends(require_admin)):
    pair_id = body.get("pair_id")
    with engine.begin() as conn:
        result = conn.execute(text("SELECT registered_pair_ids FROM tournaments WHERE id = :id"), {"id": tournament_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Tournament not found")
        current = json.loads(row["registered_pair_ids"] or "[]")
        if pair_id not in current:
            current.append(pair_id)
        conn.execute(text("UPDATE tournaments SET registered_pair_ids = :rp WHERE id = :id"),
                     {"rp": json.dumps(current), "id": tournament_id})
    return {"message": "Pair registered", "registered_pair_ids": current}

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
                status = :status, current_match_id = :current_match_id
            WHERE id = :id
        """), {
            "id": court_id, "name": court["name"], "location": court["location"],
            "number": court["number"], "status": court["status"],
            "current_match_id": court.get("current_match_id"),
        })
    return {**court, "id": court_id}

# ==================== MATCHES ====================

@app.get("/api/matches")
def get_matches():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM matches ORDER BY date_time"))
        matches = []
        for row in result.mappings():
            m = dict(row)
            if isinstance(m.get("sets"), str):
                m["sets"] = json.loads(m["sets"])
            if isinstance(m.get("current_game"), str):
                m["current_game"] = json.loads(m["current_game"])
            matches.append(m)
        return matches

@app.get("/api/matches/{match_id}")
def get_match(match_id: str):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Match not found")
        m = dict(row)
        if isinstance(m.get("sets"), str):
            m["sets"] = json.loads(m["sets"])
        if isinstance(m.get("current_game"), str):
            m["current_game"] = json.loads(m["current_game"])
        return m

@app.put("/api/matches/{match_id}")
def update_match(match_id: str, match: dict, payload: dict = Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
        if not result.mappings().first():
            raise HTTPException(status_code=404, detail="Match not found")
        conn.execute(text("""
            UPDATE matches SET tournament_id = :tournament_id, tournament_name = :tournament_name,
                court_id = :court_id, court_name = :court_name, date_time = :date_time,
                pair_a_id = :pair_a_id, pair_b_id = :pair_b_id, pair_a_name = :pair_a_name,
                pair_b_name = :pair_b_name, player_a1_id = :player_a1_id, player_a2_id = :player_a2_id,
                player_b1_id = :player_b1_id, player_b2_id = :player_b2_id,
                player_a1_name = :player_a1_name, player_a2_name = :player_a2_name,
                player_b1_name = :player_b1_name, player_b2_name = :player_b2_name,
                player_a1_avatar = :player_a1_avatar, player_a2_avatar = :player_a2_avatar,
                player_b1_avatar = :player_b1_avatar, player_b2_avatar = :player_b2_avatar,
                status = :status, sets = :sets, current_game = :current_game,
                current_set_index = :current_set_index, winner_pair_id = :winner_pair_id,
                winner_team = :winner_team, start_time_ms = :start_time_ms,
                elapsed_time_sec = :elapsed_time_sec, golden_point = :golden_point,
                sets_to_win = :sets_to_win, round_name = :round_name
            WHERE id = :id
        """), {
            "id": match_id,
            "tournament_id": match.get("tournament_id"), "tournament_name": match.get("tournament_name"),
            "court_id": match.get("court_id"), "court_name": match["court_name"],
            "date_time": match["date_time"], "pair_a_id": match["pair_a_id"], "pair_b_id": match["pair_b_id"],
            "pair_a_name": match["pair_a_name"], "pair_b_name": match["pair_b_name"],
            "player_a1_id": match["player_a1_id"], "player_a2_id": match["player_a2_id"],
            "player_b1_id": match["player_b1_id"], "player_b2_id": match["player_b2_id"],
            "player_a1_name": match["player_a1_name"], "player_a2_name": match["player_a2_name"],
            "player_b1_name": match["player_b1_name"], "player_b2_name": match["player_b2_name"],
            "player_a1_avatar": match.get("player_a1_avatar"), "player_a2_avatar": match.get("player_a2_avatar"),
            "player_b1_avatar": match.get("player_b1_avatar"), "player_b2_avatar": match.get("player_b2_avatar"),
            "status": match["status"], "sets": json.dumps(match.get("sets", [])),
            "current_game": json.dumps(match.get("current_game", {})),
            "current_set_index": match.get("current_set_index", 0),
            "winner_pair_id": match.get("winner_pair_id"), "winner_team": match.get("winner_team"),
            "start_time_ms": match.get("start_time_ms"), "elapsed_time_sec": match.get("elapsed_time_sec", 0),
            "golden_point": match.get("golden_point", False), "sets_to_win": match.get("sets_to_win", 2),
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
        conn.execute(text("UPDATE matches SET court_id = :cid, court_name = :cname WHERE id = :id"),
                     {"cid": court_id, "cname": court_name, "id": match_id})
    return {"message": "Court updated", "court_id": court_id, "court_name": court_name}

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
            INSERT INTO audit_logs (id, admin_name, admin_email, action, target, details, timestamp)
            VALUES (:id, :admin_name, :admin_email, :action, :target, :details, :timestamp)
            ON CONFLICT (id) DO UPDATE SET
                admin_name = EXCLUDED.admin_name, admin_email = EXCLUDED.admin_email,
                action = EXCLUDED.action, target = EXCLUDED.target,
                details = EXCLUDED.details, timestamp = EXCLUDED.timestamp
        """), {
            "id": log["id"], "admin_name": log["admin_name"], "admin_email": log["admin_email"],
            "action": log["action"], "target": log["target"], "details": log.get("details"),
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
            INSERT INTO notifications (id, title, body, timestamp, read, type, link_id)
            VALUES (:id, :title, :body, :timestamp, :read, :type, :link_id)
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title, body = EXCLUDED.body, timestamp = EXCLUDED.timestamp,
                read = EXCLUDED.read, type = EXCLUDED.type, link_id = EXCLUDED.link_id
        """), {
            "id": notification["id"], "title": notification["title"], "body": notification.get("body"),
            "timestamp": notification["timestamp"], "read": notification.get("read", False),
            "type": notification["type"], "link_id": notification.get("link_id"),
        })
    return notification

# ==================== STATS ====================

@app.get("/api/stats")
def get_stats():
    with engine.connect() as conn:
        total_matches = conn.execute(text("SELECT COUNT(*) FROM matches")).scalar()
        total_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments")).scalar()
        total_players = conn.execute(text("SELECT COUNT(*) FROM users WHERE role = 'PLAYER'")).scalar()
        total_pairs = conn.execute(text("SELECT COUNT(*) FROM pairs")).scalar()
        total_courts = conn.execute(text("SELECT COUNT(*) FROM courts")).scalar()
        total_notifications = conn.execute(text("SELECT COUNT(*) FROM notifications")).scalar()
        total_audit_logs = conn.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar()

        live_matches = conn.execute(text("SELECT COUNT(*) FROM matches WHERE status = 'LIVE'")).scalar()
        upcoming_matches = conn.execute(text("SELECT COUNT(*) FROM matches WHERE status = 'UPCOMING'")).scalar()
        finished_matches = conn.execute(text("SELECT COUNT(*) FROM matches WHERE status = 'FINISHED'")).scalar()

        active_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments WHERE status = 'ACTIVE'")).scalar()
        registration_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments WHERE status = 'REGISTRATION'")).scalar()
        upcoming_tournaments = conn.execute(text("SELECT COUNT(*) FROM tournaments WHERE status = 'UPCOMING'")).scalar()

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
                "registration": registration_tournaments,
                "upcoming": upcoming_tournaments
            }
        }

# ==================== DB DIRECT QUERIES ====================

@app.get("/api/db/users")
def db_get_users(payload: dict = Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users ORDER BY points DESC"))
        users = []
        for row in result.mappings():
            user = dict(row)
            if isinstance(user.get("stats"), str):
                user["stats"] = json.loads(user["stats"])
            if not user.get("stats"):
                user["stats"] = {}
            users.append(user)
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
            if isinstance(m.get("current_game"), str):
                m["current_game"] = json.loads(m["current_game"])
            matches.append(m)
        return matches
