"""Validation service - domain validation logic."""

from domain.exceptions import ValidationError


class ValidationService:
    @staticmethod
    def validate_pair_players(player1_id: str, player2_id: str) -> None:
        if player1_id == player2_id:
            raise ValidationError("Pair players must be different")

    @staticmethod
    def validate_match_pair_references(pair_a_id: str | None, pair_b_id: str | None) -> None:
        if not pair_a_id or not pair_b_id:
            raise ValidationError("Match must have both pairs")
        if pair_a_id == pair_b_id:
            raise ValidationError("Match pairs must be different")

    @staticmethod
    def validate_tournament_registration(pair_id: str, tournament_id: str) -> None:
        if not pair_id or not tournament_id:
            raise ValidationError("Tournament registration requires pair and tournament IDs")
