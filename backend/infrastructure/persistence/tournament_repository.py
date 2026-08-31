import json
from typing import Optional, List, Dict, Any

from sqlalchemy import text

from domain.repositories.tournament_repository import TournamentRepository
from domain.value_objects.tournament_status import TournamentStatus
from domain.services.tournament_rules_service import TournamentRulesService
from infrastructure.config.database import engine
from infrastructure.mappers.response_builder import TournamentResponseBuilder


class SqlTournamentRepository(TournamentRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM tournaments ORDER BY start_date"))
            tournaments = []
            for row in result.mappings():
                t = dict(row)
                t["registered_pair_ids"] = [r["pair_id"] for r in conn.execute(text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"), {"tid": t["id"]}).mappings()]
                t["registered_user_ids"] = [r["user_id"] for r in conn.execute(text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"), {"tid": t["id"]}).mappings()]
                tournaments.append(TournamentResponseBuilder.build(t))
            return tournaments

    def get_by_id(self, tournament_id: str) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
            row = result.mappings().first()
            if not row:
                return None
            t = dict(row)
            t["registered_pair_ids"] = [r["pair_id"] for r in conn.execute(text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
            t["registered_user_ids"] = [r["user_id"] for r in conn.execute(text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
            return TournamentResponseBuilder.build(t)

    def get_full(self, tournament_id: str) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            t = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id}).mappings().first()
            if not t:
                return None
            t = dict(t)

            categories = conn.execute(text("""
                SELECT * FROM tournament_categories WHERE tournament_id = :tid ORDER BY name
            """), {"tid": tournament_id}).mappings().all()
            t["categories"] = [dict(c) for c in categories]

            rounds = conn.execute(text("""
                SELECT * FROM tournament_rounds WHERE tournament_id = :tid ORDER BY round_number
            """), {"tid": tournament_id}).mappings().all()
            t["rounds"] = [dict(r) for r in rounds]

            tp_rows = conn.execute(text("""
                SELECT tp.*, p.name as pair_name, p.player1_id, p.player2_id,
                       u1.name as p1_name, u1.surname as p1_surname, u1.avatar as p1_avatar,
                       u2.name as p2_name, u2.surname as p2_surname, u2.avatar as p2_avatar
                FROM tournament_pairs tp
                JOIN pairs p ON tp.pair_id = p.id
                JOIN users u1 ON p.player1_id = u1.id
                JOIN users u2 ON p.player2_id = u2.id
                WHERE tp.tournament_id = :tid
                ORDER BY tp.seed
            """), {"tid": tournament_id}).mappings().all()
            t["registered_pairs"] = [dict(r) for r in tp_rows]

            tpl_rows = conn.execute(text("""
                SELECT tpl.*, u.name, u.surname, u.username, u.avatar, u.points
                FROM tournament_players tpl
                JOIN users u ON tpl.user_id = u.id
                WHERE tpl.tournament_id = :tid
                ORDER BY u.surname
            """), {"tid": tournament_id}).mappings().all())
            t["registered_players"] = [dict(r) for r in tpl_rows]

            match_rows = conn.execute(text("""
                SELECT m.id, m.court_id, m.pair_a_id, m.pair_b_id, m.round_name,
                       m.date_time, m.status, m.sets, m.winner_team, m.current_set_index,
                       m.sets_to_win, m.golden_point, m.round_id,
                       pa.name as pair_a_name, pb.name as pair_b_name
                FROM matches m
                LEFT JOIN pairs pa ON m.pair_a_id = pa.id
                LEFT JOIN pairs pb ON m.pair_b_id = pb.id
                WHERE m.tournament_id = :tid
                ORDER BY m.date_time
            """), {"tid": tournament_id}).mappings().all()
            matches = []
            for r in match_rows:
                m = dict(r)
                if isinstance(m.get("sets"), str):
                    m["sets"] = json.loads(m["sets"])
                matches.append(m)
            t["matches"] = matches

            rules = t.get("rules")
            if isinstance(rules, str):
                try:
                    rules = json.loads(rules)
                except Exception:
                    rules = {}
            t["rules"] = rules

            return t
        return None

    def create(self, tournament_data: Dict[str, Any]) -> Dict[str, Any]:
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
                "id": tournament_data["id"], "business_id": tournament_data.get("business_id"),
                "created_by": tournament_data.get("created_by"), "name": tournament_data["name"],
                "logo": tournament_data.get("logo"), "description": tournament_data.get("description"),
                "category": tournament_data.get("category"), "level": tournament_data.get("level"),
                "location": tournament_data.get("location"), "start_date": tournament_data.get("start_date"),
                "end_date": tournament_data.get("end_date"), "status": tournament_data.get("status", "DRAFT"),
                "format": tournament_data.get("format"), "max_pairs": tournament_data.get("max_pairs"),
                "visibility": tournament_data.get("visibility", "PRIVATE"),
                "rules": json.dumps(tournament_data.get("rules", {})),
            })
        return tournament_data

    def update(self, tournament_id: str, tournament_data: Dict[str, Any]) -> Dict[str, Any]:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
            if not result.mappings().first():
                raise ValueError("Tournament not found")
            conn.execute(text("""
                UPDATE tournaments SET
                    name = :name, logo = :logo, description = :description, category = :category,
                    level = :level, location = :location, start_date = :start_date, end_date = :end_date,
                    status = :status, format = :format, max_pairs = :max_pairs,
                    visibility = :visibility, rules = :rules
                WHERE id = :id
            """), {
                "id": tournament_id,
                "name": tournament_data.get("name"), "logo": tournament_data.get("logo"),
                "description": tournament_data.get("description"), "category": tournament_data.get("category"),
                "level": tournament_data.get("level"), "location": tournament_data.get("location"),
                "start_date": tournament_data.get("start_date"), "end_date": tournament_data.get("end_date"),
                "status": tournament_data.get("status"), "format": tournament_data.get("format"),
                "max_pairs": tournament_data.get("max_pairs"),
                "visibility": tournament_data.get("visibility", "PRIVATE"),
                "rules": json.dumps(tournament_data.get("rules", {})),
            })
        return {**tournament_data, "id": tournament_id}

    def delete(self, tournament_id: str) -> None:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
            if not result.mappings().first():
                raise ValueError("Tournament not found")
            conn.execute(text("DELETE FROM matches WHERE tournament_id = :tid"), {"tid": tournament_id})
            conn.execute(text("DELETE FROM tournaments WHERE id = :tid"), {"tid": tournament_id})

    def get_registered_pair_ids(self, tournament_id: str) -> List[str]:
        with engine.connect() as conn:
            return [r["pair_id"] for r in conn.execute(text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]

    def get_registered_user_ids(self, tournament_id: str) -> List[str]:
        with engine.connect() as conn:
            return [r["user_id"] for r in conn.execute(text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]

    def register_pair(self, tournament_id: str, pair_id: Optional[str]) -> List[str]:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
            if not result.mappings().first():
                raise ValueError("Tournament not found")
            conn.execute(text("""
                INSERT INTO tournament_pairs (tournament_id, pair_id, status) VALUES (:tid, :pid, 'REGISTERED')
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """), {"tid": tournament_id, "pid": pair_id})
            registered = [r["pair_id"] for r in conn.execute(text("SELECT pair_id FROM tournament_pairs WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
        return registered

    def register_user(self, tournament_id: str, user_id: Optional[str]) -> List[str]:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM tournaments WHERE id = :id"), {"id": tournament_id})
            if not result.mappings().first():
                raise ValueError("Tournament not found")
            conn.execute(text("""
                INSERT INTO tournament_players (tournament_id, user_id, status) VALUES (:tid, :uid, 'REGISTERED')
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """), {"tid": tournament_id, "uid": user_id})
            registered = [r["user_id"] for r in conn.execute(text("SELECT user_id FROM tournament_players WHERE tournament_id = :tid"), {"tid": tournament_id}).mappings()]
        return registered
