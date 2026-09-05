"""Matches use cases."""

import json
from domain.exceptions import EntityNotFound


def _normalize_set(s: dict) -> dict:
    return {
        "teamAGames": s.get("team_a_games") or s.get("teamAGames") or 0,
        "teamBGames": s.get("team_b_games") or s.get("teamBGames") or 0,
        "isTieBreak": s.get("is_tie_break") if s.get("is_tie_break") is not None else s.get("isTieBreak") or False,
        "tieBreakPoints": s.get("tie_break_points") or s.get("tieBreakPoints") or {"teamA": 0, "teamB": 0},
        "winner": s.get("winner"),
    }


def _normalize_current_game(cg: dict) -> dict:
    if not cg:
        return {"teamAPoints": "0", "teamBPoints": "0", "serverTeam": "A", "isDeuce": False}
    return {
        "teamAPoints": cg.get("team_a_points") or cg.get("teamAPoints") or "0",
        "teamBPoints": cg.get("team_b_points") or cg.get("teamBPoints") or "0",
        "serverTeam": cg.get("server_team") or cg.get("serverTeam") or "A",
        "isDeuce": cg.get("is_deuce") if cg.get("is_deuce") is not None else cg.get("isDeuce") or False,
    }


def _normalize_match_status(status: str | None) -> str:
    if not status:
        return "UPCOMING"
    s = str(status).strip().upper()
    if s == "IN_PROGRESS":
        return "LIVE"
    if s == "SCHEDULED":
        return "UPCOMING"
    return s


class ListMatchesUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self):
        rows = self.match_repo.find_all_detailed()
        result = []
        for m in rows:
            if isinstance(m.get("sets"), str):
                m["sets"] = json.loads(m["sets"])
            m["status"] = _normalize_match_status(m.get("status"))
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
            m["sets"] = [_normalize_set(s) for s in (m.get("sets") or [])]
            m["current_game"] = _normalize_current_game(m.get("current_game") or {})
            result.append(m)
        return result


class GetMatchUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self, match_id):
        m = self.match_repo.find_by_id_detailed(match_id)
        if not m:
            raise EntityNotFound("Match not found")
        if isinstance(m.get("sets"), str):
            m["sets"] = json.loads(m["sets"])
        m["status"] = _normalize_match_status(m.get("status"))
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
        m["sets"] = [_normalize_set(s) for s in (m.get("sets") or [])]
        m["current_game"] = _normalize_current_game(m.get("current_game") or {})
        return m


class GetMatchPlayersUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self, match_id):
        return self.match_repo.find_players(match_id)


class CreateMatchUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self, match_data):
        from domain.entities.match import Match
        m = Match(
            match_id=match_data["id"],
            tournament_id=match_data.get("tournament_id"),
            pair_a_id=match_data.get("pair_a_id") or match_data.get("pairAId"),
            pair_b_id=match_data.get("pair_b_id") or match_data.get("pairBId"),
            date_time=match_data.get("date_time") or match_data.get("dateTime"),
            status=match_data.get("status", "SCHEDULED"),
            court_id=match_data.get("court_id") or match_data.get("courtId"),
            round_id=match_data.get("round_id") or match_data.get("roundId"),
            business_id=match_data.get("business_id") or match_data.get("businessId"),
            created_by=match_data.get("created_by", ""),
            visibility=match_data.get("visibility", "PRIVATE"),
            sets=match_data.get("sets") or [],
            current_set_index=match_data.get("current_set_index", 0),
            winner_pair_id=match_data.get("winner_pair_id") or match_data.get("winnerPairId"),
            winner_team=match_data.get("winner_team") or match_data.get("winnerTeam"),
            start_time_ms=match_data.get("start_time_ms") or match_data.get("startTimeMs"),
            elapsed_time_sec=match_data.get("elapsed_time_sec", 0),
            golden_point=bool(match_data.get("golden_point") or match_data.get("goldenPoint")),
            sets_to_win=match_data.get("sets_to_win", 2),
            round_name=match_data.get("round_name") or match_data.get("roundName"),
        )
        saved = self.match_repo.save(m)
        return match_data


class UpdateMatchCourtUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self, match_id, body):
        court_id = body.get("courtId") or body.get("court_id")
        m = self.match_repo.find_by_id(match_id)
        if not m:
            raise EntityNotFound("Match not found")
        self.match_repo.update_court(match_id, court_id)
        return {"status": "updated"}


class FinishMatchUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self, match_id, body):
        m = self.match_repo.find_by_id(match_id)
        if not m:
            raise EntityNotFound("Match not found")
        winner_id = body.get("winnerPairId") or body.get("winner_pair_id")
        winner_team = body.get("winnerTeam") or body.get("winner_team")
        self.match_repo.finish(match_id, winner_id, winner_team)
        return {"status": "finished"}


class CreateMatchEventUseCase:
    def __init__(self, match_event_repo):
        self.match_event_repo = match_event_repo

    def execute(self, match_id, event_data):
        from domain.entities.match_event import MatchEvent
        event_id = event_data.get("id") or f"event_{match_id}_{event_data.get('set_number', 0)}_{event_data.get('game_number', 0)}"
        event = MatchEvent(
            event_id=event_id,
            match_id=match_id,
            event_type=event_data.get("event_type", "POINT"),
            set_number=event_data.get("set_number", 0),
            timestamp=__import__('datetime').datetime.utcnow().isoformat(),
            game_number=event_data.get("game_number"),
            winning_pair_id=event_data.get("winning_pair_id"),
            player_id=event_data.get("player_id"),
            description=event_data.get("description"),
            score_snapshot=event_data.get("score_snapshot"),
        )
        saved = self.match_event_repo.save(event)
        return event_data


class DeleteMatchUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self, match_id):
        m = self.match_repo.find_by_id(match_id)
        if not m:
            raise EntityNotFound("Match not found")
        self.match_repo.delete(match_id)
        return {"message": "Match deleted"}


