"""Scoring service - padel scoring domain logic."""

from typing import Any, Tuple
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
        golden_point = match.get("goldenPoint", False)
        server_team = current_set.get("server_team", "A")

        if team == "A":
            team_a_points, team_b_points = self._advance_point(team_a_points, team_b_points, golden_point)
        else:
            team_b_points, team_a_points = self._advance_point(team_b_points, team_a_points, golden_point)

        current_set["team_a_points"] = team_a_points
        current_set["team_b_points"] = team_b_points
        current_set["server_team"] = "A" if server_team == "B" else "B"

        game_winner = self._check_game_winner(team_a_points, team_b_points)
        if game_winner:
            current_set["team_a_points"] = "0"
            current_set["team_b_points"] = "0"
            current_set["server_team"] = "A"
            if game_winner == "A":
                current_set["team_a_games"] = current_set.get("team_a_games", 0) + 1
            else:
                current_set["team_b_games"] = current_set.get("team_b_games", 0) + 1

            games_a = current_set.get("team_a_games", 0)
            games_b = current_set.get("team_b_games", 0)
            is_tie_break = current_set.get("is_tie_break", False)

            if is_tie_break:
                if games_a > games_b:
                    current_set["winner"] = "A"
                else:
                    current_set["winner"] = "B"
            else:
                if games_a >= 6 and games_a - games_b >= 2:
                    current_set["winner"] = "A"
                elif games_b >= 6 and games_b - games_a >= 2:
                    current_set["winner"] = "B"
                elif games_a == 6 and games_b == 6:
                    current_set["is_tie_break"] = True
                    current_set["team_a_points"] = "0"
                    current_set["team_b_points"] = "0"

        match["sets"] = sets
        return match

    def _advance_point(self, my_points: str, opponent_points: str, golden_point: bool) -> Tuple[str, str]:
        if golden_point and is_deuce(my_points, opponent_points):
            return "GAME", opponent_points

        if my_points == "40" and opponent_points == "40":
            return "AD", opponent_points

        if my_points == "40" and opponent_points == "AD":
            return "40", "40"

        if my_points == "AD":
            return "GAME", opponent_points

        if my_points == "40" and opponent_points != "40" and opponent_points != "AD":
            return "GAME", opponent_points

        if my_points in POINT_SEQUENCE:
            return next_point(my_points), opponent_points

        return my_points, opponent_points

    def _check_game_winner(self, team_a: str, team_b: str) -> str | None:
        if team_a == "GAME":
            return "A"
        if team_b == "GAME":
            return "B"
        return None
