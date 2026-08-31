import json
from typing import Optional, List, Tuple, Dict, Any

from sqlalchemy import text

from domain.repositories.match_repository import MatchRepository
from domain.services.scoring_service import ScoringService
from domain.value_objects.match_status import MatchStatus
from infrastructure.config.database import engine
from infrastructure.transformers.match_transformer import normalize_match_payload
from infrastructure.mappers.response_builder import MatchResponseBuilder
from infrastructure.persistence.pair_repository import SqlPairRepository


class SqlMatchRepository(MatchRepository):
    MATCH_SELECT = """
        SELECT m.id,
            m.tournament_id AS tournamentId,
            m.round_id AS roundId,
            m.business_id AS businessId,
            m.court_id AS courtId,
            m.created_by AS createdBy,
            m.pair_a_id AS pairAId,
            m.pair_b_id AS pairBId,
            pa.player1_id AS playerA1Id,
            pa.player2_id AS playerA2Id,
            pb.player1_id AS playerB1Id,
            pb.player2_id AS playerB2Id,
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
        LEFT JOIN users ua1 ON pa.player1_id = ua1.id
        LEFT JOIN users ua2 ON pa.player2_id = ua2.id
        LEFT JOIN users ub1 ON pb.player1_id = ub1.id
        LEFT JOIN users ub2 ON pb.player2_id = ub2.id
    """

    MATCH_SELECT_FALLBACK = """
        SELECT m.id,
            m.tournament_id AS tournamentId,
            m.court_id AS courtId,
            m.created_by AS createdBy,
            m.pair_a_id AS pairAId,
            m.pair_b_id AS pairBId,
            pa.player1_id AS playerA1Id,
            pa.player2_id AS playerA2Id,
            pb.player1_id AS playerB1Id,
            pb.player2_id AS playerB2Id,
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
        LEFT JOIN users ua1 ON pa.player1_id = ua1.id
        LEFT JOIN users ua2 ON pa.player2_id = ua2.id
        LEFT JOIN users ub1 ON pb.player1_id = ub1.id
        LEFT JOIN users ub2 ON pb.player2_id = ub2.id
    """

    def get_all(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            try:
                result = conn.execute(text(self.MATCH_SELECT + " ORDER BY m.date_time"))
            except Exception:
                result = conn.execute(text(self.MATCH_SELECT_FALLBACK + " ORDER BY m.date_time"))
            matches = [dict(row) for row in result.mappings()]
        matches = MatchResponseBuilder.build_list(matches)
        return matches

    def get_by_id(self, match_id: str) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            try:
                result = conn.execute(text(self.MATCH_SELECT + " WHERE m.id = :id"), {"id": match_id})
            except Exception:
                result = conn.execute(text(self.MATCH_SELECT_FALLBACK + " WHERE m.id = :id"), {"id": match_id})
            row = result.mappings().first()
            if not row:
                return None
            m = dict(row)
            if isinstance(m.get("sets"), str):
                m["sets"] = json.loads(m["sets"])
            m["current_game"] = {}
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
            return m

    def create(self, match_data: Dict[str, Any]) -> Dict[str, Any]:
        match = normalize_match_payload(match_data)
        with engine.begin() as conn:
            pair_a_id = match.get("pair_a_id")
            pair_b_id = match.get("pair_b_id")
            if pair_a_id or pair_b_id:
                valid, msg = self.validate_pair_references(conn, pair_a_id, pair_b_id)
                if not valid:
                    raise ValueError(msg)

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
                "pair_a_id": pair_a_id, "pair_b_id": pair_b_id,
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

            if pair_a_id or pair_b_id:
                self.sync_match_players_from_pairs(conn, match["id"])

        return match

    def update(self, match_id: str, match_data: Dict[str, Any]) -> Dict[str, Any]:
        match = normalize_match_payload(match_data)
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
            if not result.mappings().first():
                raise ValueError("Match not found")
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

    def delete(self, match_id: str) -> None:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
            if not result.mappings().first():
                raise ValueError("Match not found")
            conn.execute(text("DELETE FROM matches WHERE id = :id"), {"id": match_id})

    def get_players(self, match_id: str) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT mp.match_id, mp.user_id, mp.pair_id, mp.team, mp.player_number,
                       u.name, u.surname, u.avatar, u.username
                FROM match_players mp
                JOIN users u ON mp.user_id = u.id
                WHERE mp.match_id = :mid
                ORDER BY mp.team, mp.player_number
            """), {"mid": match_id}).mappings().all()
        return [dict(r) for r in rows]

    def update_court(self, match_id: str, court_id: Optional[str], court_name: Optional[str]) -> Dict[str, Any]:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
            if not result.mappings().first():
                raise ValueError("Match not found")
            conn.execute(text("UPDATE matches SET court_id = :cid WHERE id = :id"),
                         {"cid": court_id, "id": match_id})
        return {"message": "Court updated", "court_id": court_id, "court_name": court_name}

    def finish(self, match_id: str, winner_team: str, sets: List[Dict[str, Any]]) -> None:
        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM matches WHERE id = :id"), {"id": match_id})
            row = result.mappings().first()
            if not row:
                raise ValueError("Match not found")
            match = dict(row)
            if isinstance(match.get("sets"), str):
                match["sets"] = json.loads(match["sets"])

            winner_team = ScoringService.determine_winner_team(winner_team, sets)
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
            """), {"id": match_id, "winner_team": winner_team})

            for pid in winner_player_ids:
                if not pid:
                    continue
                sets = match.get("sets", [])
                player_winner = "A" if is_winner_a else "B"
                base_points = ScoringService.get_base_points(True)
                sets_won = sum(1 for s in sets if s.get("winner") == player_winner)
                conn.execute(text("""
                    INSERT INTO user_points (user_id, match_id, points, reason)
                    VALUES (:uid, :mid, :pts, :reason)
                """), {"uid": pid, "mid": match_id, "pts": base_points, "reason": "match_finish_winner"})
                conn.execute(text("""
                    UPDATE users SET points = points + :pts WHERE id = :uid
                """), {"pts": base_points, "uid": pid})

            for pid in loser_player_ids:
                if not pid:
                    continue
                sets = match.get("sets", [])
                player_winner = "B" if is_winner_a else "A"
                base_points = ScoringService.get_base_points(False)
                sets_won = sum(1 for s in sets if s.get("winner") == player_winner)
                conn.execute(text("""
                    INSERT INTO user_points (user_id, match_id, points, reason)
                    VALUES (:uid, :mid, :pts, :reason)
                """), {"uid": pid, "mid": match_id, "pts": base_points, "reason": "match_finish_loser"})
                conn.execute(text("""
                    UPDATE users SET points = points + :pts WHERE id = :uid
                """), {"pts": base_points, "uid": pid})

        return {"message": "Match finished", "match_id": match_id, "winner_team": winner_team}

    def create_event(self, event_data: Dict[str, Any], match_id: str) -> Dict[str, Any]:
        event = normalize_match_payload(event_data)
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

    def sync_match_players_from_pairs(self, conn, match_id: str) -> List[Dict[str, Any]]:
        match = conn.execute(text("SELECT pair_a_id, pair_b_id FROM matches WHERE id = :id"), {"id": match_id}).mappings().first()
        if not match:
            return []
        conn.execute(text("DELETE FROM match_players WHERE match_id = :id"), {"id": match_id})
        inserted = []
        team_mapping = [("A", match["pair_a_id"]), ("B", match["pair_b_id"])]
        for team, pair_id in team_mapping:
            if not pair_id:
                continue
            pair = conn.execute(text("SELECT player1_id, player2_id FROM pairs WHERE id = :id"), {"id": pair_id}).mappings().first()
            if not pair:
                continue
            for idx, uid in enumerate([pair["player1_id"], pair["player2_id"]], 1):
                if not uid:
                    continue
                conn.execute(text("""
                    INSERT INTO match_players (match_id, user_id, pair_id, team, player_number)
                    VALUES (:mid, :uid, :pid, :team, :pn)
                    ON DUPLICATE KEY UPDATE pair_id = VALUES(pair_id), team = VALUES(team)
                """), {"mid": match_id, "uid": uid, "pid": pair_id, "team": team, "pn": idx})
                inserted.append({"user_id": uid, "pair_id": pair_id, "team": team, "player_number": idx})
        return inserted

    def validate_pair_references(self, conn, pair_a_id: Optional[str], pair_b_id: Optional[str]) -> Tuple[bool, str]:
        pair_repo = SqlPairRepository()
        for label, pid in [("pair_a_id", pair_a_id), ("pair_b_id", pair_b_id)]:
            if not pid:
                continue
            r = conn.execute(text("SELECT player1_id, player2_id FROM pairs WHERE id = :id"), {"id": pid}).mappings().first()
            if not r:
                return False, f"Pair '{pid}' ({label}) does not exist"
            valid, msg = pair_repo.validate_players_exist(r["player1_id"], r["player2_id"])
            if not valid:
                return False, f"Invalid players in {label} '{pid}': {msg}"
        return True, ""
