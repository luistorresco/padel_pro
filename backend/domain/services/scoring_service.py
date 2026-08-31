"""Scoring service - padel scoring domain logic."""

from typing import Any
from domain.value_objects.scoring import POINT_SEQUENCE, next_point, is_deuce, has_advantage


class ScoringService:
    def award_point(self, match: dict, team: str, event_type: str) -> dict:
        sets = match.get("sets", [])
        current_set_idx = match.get("currentSetIndex", 0)
        if current_set_idx >= len(sets):
            return match

        current_set = sets[current_set_idx]
        team_a_points = current_set.get("team_a_points", "0")
        team_b_points = current_set.get("team_b_points", "0")

        if team == "A":
            team_a_points = self._advance_point(team_a_points, team_b_points)
        else:
            team_b_points = self._advance_point(team_b_points, team_a_points)

        current_set["team_a_points"] = team_a_points
        current_set["team_b_points"] = team_b_points
        current_set["server_team"] = team

        game_winner = self._check_game_winner(team_a_points, team_b_points, match.get("goldenPoint", False))
        if game_winner:
            current_set["winner"] = game_winner
            current_set["is_tie_break"] = False
            match["currentSetIndex"] = current_set_idx + 1

        match["sets"] = sets
        return match

    def _advance_point(self, my_points: str, opponent_points: str) -> str:
        if my_points == "40" and opponent_points != "40" and opponent_points != "AD":
            return "GAME"
        if my_points == "40" and opponent_points == "40":
            return "AD"
        if my_points == "AD":
            return "GAME"
        if my_points in POINT_SEQUENCE:
            return next_point(my_points)
        return my_points

    def _check_game_winner(self, team_a: str, team_b: str, golden_point: bool) -> str | None:
        if team_a == "GAME":
            return "A"
        if team_b == "GAME":
            return "B"
        return None
