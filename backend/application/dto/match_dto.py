"""Match DTOs."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MatchCreateDTO:
    tournament_id: str
    pair_a_id: str
    pair_b_id: str
    date_time: str
    court_id: str | None = None
    round_id: str | None = None
    business_id: str | None = None
    created_by: str = ""
    visibility: str = "PRIVATE"
    golden_point: bool = False
    sets_to_win: int = 2
    round_name: str | None = None


@dataclass
class MatchResponseDTO:
    id: str
    tournament_id: str | None
    pair_a_id: str | None
    pair_b_id: str | None
    date_time: str | None
    status: str
    court_id: str | None
    court_name: str
    tournament_name: str
    pair_a_name: str
    pair_b_name: str
    player_a1_name: str
    player_a2_name: str
    player_b1_name: str
    player_b2_name: str
    player_a1_avatar: str
    player_a2_avatar: str
    player_b1_avatar: str
    player_b2_avatar: str
    sets: list
    current_set_index: int
    visibility: str
    golden_point: bool
    sets_to_win: int
    round_name: str | None
    created_at: str | None
    updated_at: str | None
