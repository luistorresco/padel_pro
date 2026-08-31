"""Bracket service - tournament bracket logic."""

from typing import Optional
from domain.entities.match import Match
from domain.entities.tournament import Tournament
from domain.value_objects.status import MatchStatus


class BracketService:
    @staticmethod
    def get_next_round_name(current_round: str) -> str | None:
        mapping = {
            "Cuartos de Final": "Semifinal",
            "Semifinal": "Gran Final",
            "Round of 16": "Quarterfinal",
            "Quarterfinal": "Semifinal",
            "Semifinal": "Final",
        }
        return mapping.get(current_round)

    @staticmethod
    def create_next_match(
        current_match: Match,
        tournament: Tournament,
        next_round_name: str,
        winner_pair_id: str,
        winner_pair_name: str,
    ) -> Match:
        return Match(
            match_id=f"match_auto_{current_match.id}",
            tournament_id=tournament.id,
            pair_a_id=winner_pair_id,
            pair_b_id=None,
            date_time=None,
            status=MatchStatus.SCHEDULED,
            court_id=current_match.court_id,
            round_name=next_round_name,
            created_by=current_match.created_by,
            visibility=tournament.visibility,
            sets=[],
            current_set_index=0,
            golden_point=bool(tournament.rules.get("goldenPoint", False)),
            sets_to_win=int(tournament.rules.get("setsToWin", 2)),
        )
