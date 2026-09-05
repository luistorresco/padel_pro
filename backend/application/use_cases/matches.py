"""Matches use cases."""

import json
import random
from datetime import datetime
from domain.exceptions import EntityNotFound
from domain.entities.pair import Pair


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


class UpdateMatchDateTimeUseCase:
    def __init__(self, match_repo):
        self.match_repo = match_repo

    def execute(self, match_id, body):
        m = self.match_repo.find_by_id(match_id)
        if not m:
            raise EntityNotFound("Match not found")
        date_time = body.get("dateTime") or body.get("date_time")
        if not date_time:
            raise ValueError("date_time is required")
        with self.match_repo.engine.begin() as conn:
            conn.execute(text("UPDATE matches SET date_time = :dt WHERE id = :id"), {"dt": date_time, "id": match_id})
        return {"status": "updated", "date_time": date_time}


class FinishMatchUseCase:
    def __init__(self, match_repo, user_repo, user_points_repo, pair_repo):
        self.match_repo = match_repo
        self.user_repo = user_repo
        self.user_points_repo = user_points_repo
        self.pair_repo = pair_repo

    def execute(self, match_id, body):
        m = self.match_repo.find_by_id(match_id)
        if not m:
            raise EntityNotFound("Match not found")
        winner_id = body.get("winnerPairId") or body.get("winner_pair_id")
        winner_team = body.get("winnerTeam") or body.get("winner_team")
        self.match_repo.finish(match_id, winner_id, winner_team)

        if m.pair_a_id and m.pair_b_id and winner_id:
            self._award_stats_and_points(m, winner_id)

        return {"status": "finished"}

    def _award_stats_and_points(self, match, winner_pair_id):
        try:
            winner_pair = self.user_repo.find_pair_with_players(winner_pair_id)
            if not winner_pair:
                return
            winner_player_ids = [winner_pair.get("player1_id"), winner_pair.get("player2_id")]

            loser_pair_id = match.pair_b_id if match.pair_a_id == winner_pair_id else match.pair_a_id
            loser_pair = None
            loser_player_ids = []
            if loser_pair_id:
                loser_pair = self.user_repo.find_pair_with_players(loser_pair_id)
                if loser_pair:
                    loser_player_ids = [loser_pair.get("player1_id"), loser_pair.get("player2_id")]

            tournament = None
            if match.tournament_id:
                try:
                    tournament = self.user_repo.find_tournament_rules(match.tournament_id)
                except Exception:
                    pass

            points_map = {
                "champion": 1000,
                "runner_up": 600,
                "semi_finals": 360,
                "quarter_finals": 180,
                "group_stage": 90,
                "match_win": 150,
            }
            if tournament and isinstance(tournament, dict):
                rules = tournament.get("rules") or {}
                if isinstance(rules, str):
                    try:
                        rules = json.loads(rules)
                    except Exception:
                        rules = {}
                points_map.update(rules.get("pointsDistribution", {}))

            round_name = match.round_name or ""
            reason = "match_win"
            points = points_map.get("match_win", 150)
            if "FINAL" in round_name.upper() or "GRAN FINAL" in round_name.upper():
                reason = "champion"
                points = points_map.get("champion", 1000)
            elif "SEMIFINAL" in round_name.upper():
                reason = "semi_finals"
                points = points_map.get("semi_finals", 360)
            elif "CUARTOS" in round_name.upper() or "QUARTERFINAL" in round_name.upper():
                reason = "quarter_finals"
                points = points_map.get("quarter_finals", 180)
            elif "GRUPO" in round_name.upper() or "GROUP" in round_name.upper():
                reason = "group_stage"
                points = points_map.get("group_stage", 90)

            sets = match.sets or []
            winner_sets = sum(1 for s in sets if s.get("winner") == ('A' if match.pair_a_id == winner_pair_id else 'B'))
            loser_sets = sum(1 for s in sets if s.get("winner") == ('A' if match.pair_a_id == loser_pair_id else 'B'))
            if not winner_sets and not loser_sets and sets:
                winner_sets = len([s for s in sets if s.get("teamAGames", 0) > s.get("teamBGames", 0)])
                loser_sets = len([s for s in sets if s.get("teamBGames", 0) > s.get("teamAGames", 0)])

            winner_games = sum(s.get("teamAGames" if match.pair_a_id == winner_pair_id else "teamBGames", 0) for s in sets)
            loser_games = sum(s.get("teamAGames" if match.pair_a_id == loser_pair_id else "teamBGames", 0) for s in sets)

            for pid in winner_player_ids:
                if not pid:
                    continue
                try:
                    self.user_points_repo.save({
                        "user_id": pid,
                        "match_id": match.id,
                        "tournament_id": match.tournament_id,
                        "points": points,
                        "reason": reason,
                        "created_at": datetime.utcnow().isoformat(),
                    })
                except Exception:
                    pass

                try:
                    current = self.user_repo.find_by_id(pid)
                    if current:
                        updated = User(
                            user_id=pid,
                            name=current.name,
                            surname=current.surname,
                            username=current.username,
                            email=current.email,
                            avatar=current.avatar,
                            account_type=current.account_type,
                            status=current.status,
                            level=current.level,
                            position=current.position,
                            dominant_hand=current.dominant_hand,
                            points=(current.points or 0) + points,
                            invited_by=current.invited_by,
                            invitation_code=current.invitation_code,
                            converted_at=current.converted_at,
                            deleted_at=current.deleted_at,
                            created_at=current.created_at,
                            updated_at=current.updated_at,
                            matches_played=(getattr(current, 'matches_played', 0) or 0) + 1,
                            matches_won=(getattr(current, 'matches_won', 0) or 0) + 1,
                            matches_lost=getattr(current, 'matches_lost', 0) or 0,
                            sets_won=(getattr(current, 'sets_won', 0) or 0) + winner_sets,
                            sets_lost=(getattr(current, 'sets_lost', 0) or 0) + loser_sets,
                            games_won=(getattr(current, 'games_won', 0) or 0) + winner_games,
                            games_lost=(getattr(current, 'games_lost', 0) or 0) + loser_games,
                        )
                        self.user_repo.save(updated)
                except Exception:
                    pass

            for pid in loser_player_ids:
                if not pid:
                    continue
                try:
                    current = self.user_repo.find_by_id(pid)
                    if current:
                        updated = User(
                            user_id=pid,
                            name=current.name,
                            surname=current.surname,
                            username=current.username,
                            email=current.email,
                            avatar=current.avatar,
                            account_type=current.account_type,
                            status=current.status,
                            level=current.level,
                            position=current.position,
                            dominant_hand=current.dominant_hand,
                            points=current.points or 0,
                            invited_by=current.invited_by,
                            invitation_code=current.invitation_code,
                            converted_at=current.converted_at,
                            deleted_at=current.deleted_at,
                            created_at=current.created_at,
                            updated_at=current.updated_at,
                            matches_played=(getattr(current, 'matches_played', 0) or 0) + 1,
                            matches_won=getattr(current, 'matches_won', 0) or 0,
                            matches_lost=(getattr(current, 'matches_lost', 0) or 0) + 1,
                            sets_won=(getattr(current, 'sets_won', 0) or 0) + loser_sets,
                            sets_lost=(getattr(current, 'sets_lost', 0) or 0) + winner_sets,
                            games_won=(getattr(current, 'games_won', 0) or 0) + loser_games,
                            games_lost=(getattr(current, 'games_lost', 0) or 0) + winner_games,
                        )
                        self.user_repo.save(updated)
                except Exception:
                    pass

            if match.tournament_id and winner_pair and loser_pair:
                try:
                    if "FINAL" in round_name.upper() or "GRAN FINAL" in round_name.upper():
                        self.pair_repo.save(Pair(
                            pair_id=winner_pair_id,
                            name=winner_pair.get("name", "Pareja"),
                            player1_id=winner_pair.get("player1_id"),
                            player2_id=winner_pair.get("player2_id"),
                            created_by=winner_pair.get("created_by", ""),
                            status="ACTIVE",
                            tournaments_disputed=(winner_pair.get("tournaments_disputed") or 0) + 1,
                            titles_won=(winner_pair.get("titles_won") or 0) + 1,
                        ))
                        if loser_pair:
                            self.pair_repo.save(Pair(
                                pair_id=loser_pair_id,
                                name=loser_pair.get("name", "Pareja"),
                                player1_id=loser_pair.get("player1_id"),
                                player2_id=loser_pair.get("player2_id"),
                                created_by=loser_pair.get("created_by", ""),
                                status="ACTIVE",
                                tournaments_disputed=(loser_pair.get("tournaments_disputed") or 0) + 1,
                                titles_won=loser_pair.get("titles_won") or 0,
                            ))
                    else:
                        if winner_pair.get("tournaments_disputed") is None or loser_pair.get("tournaments_disputed") is None:
                            return
                        self.pair_repo.save(Pair(
                            pair_id=winner_pair_id,
                            name=winner_pair.get("name", "Pareja"),
                            player1_id=winner_pair.get("player1_id"),
                            player2_id=winner_pair.get("player2_id"),
                            created_by=winner_pair.get("created_by", ""),
                            status="ACTIVE",
                            tournaments_disputed=winner_pair.get("tournaments_disputed", 0) + 1,
                            titles_won=winner_pair.get("titles_won", 0),
                        ))
                        self.pair_repo.save(Pair(
                            pair_id=loser_pair_id,
                            name=loser_pair.get("name", "Pareja"),
                            player1_id=loser_pair.get("player1_id"),
                            player2_id=loser_pair.get("player2_id"),
                            created_by=loser_pair.get("created_by", ""),
                            status="ACTIVE",
                            tournaments_disputed=loser_pair.get("tournaments_disputed", 0) + 1,
                            titles_won=loser_pair.get("titles_won", 0),
                        ))
                except Exception:
                    pass
        except Exception:
            pass


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


class GenerateBracketUseCase:
    def __init__(self, tournament_repo, match_repo, pair_repo):
        self.tournament_repo = tournament_repo
        self.match_repo = match_repo
        self.pair_repo = pair_repo

    def execute(self, tournament_id):
        t = self.tournament_repo.find_by_id(tournament_id)
        if not t:
            raise EntityNotFound("Tournament not found")

        full = self.tournament_repo.find_full(tournament_id)
        if not full:
            raise EntityNotFound("Tournament data not found")

        pairs = full.get("pairs", [])
        if len(pairs) < 2:
            raise ValueError("At least 2 pairs are required to generate a bracket")

        existing_matches = self.match_repo.find_by_tournament(tournament_id)
        if existing_matches:
            for match in existing_matches:
                self.match_repo.delete(match.id)

        random.shuffle(pairs)
        pair_ids = [p.get("pair_id") or p.get("id") for p in pairs if p.get("pair_id") or p.get("id")]
        pair_names = {p.get("pair_id") or p.get("id"): p.get("name", "Pareja") for p in pairs}

        rules = t.rules or {}
        if isinstance(rules, str):
            try:
                rules = json.loads(rules)
            except Exception:
                rules = {}
        golden_point = rules.get("goldenPoint") or rules.get("golden_point") or False
        sets_to_win = rules.get("setsToWin") or rules.get("sets_to_win") or 2

        matches = []
        n = len(pair_ids)
        if n >= 2:
            for i in range(0, n, 2):
                if i + 1 < n:
                    match_id = f"match_{tournament_id}_round_{i // 2}"
                    match = type('Match', (), {})()
                    match.id = match_id
                    match.tournament_id = tournament_id
                    match.pair_a_id = pair_ids[i]
                    match.pair_b_id = pair_ids[i + 1]
                    match.round_name = "Grupos"
                    match.date_time = None
                    match.status = "SCHEDULED"
                    match.court_id = None
                    match.sets = []
                    match.current_set_index = 0
                    match.winner_pair_id = None
                    match.winner_team = None
                    match.golden_point = golden_point
                    match.sets_to_win = sets_to_win
                    matches.append(match)

        for match in matches:
            self.match_repo.save(match)

        return {"generated": len(matches), "matches": [m.id for m in matches]}


