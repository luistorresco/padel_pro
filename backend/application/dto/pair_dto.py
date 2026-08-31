"""Pair DTOs."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PairCreateDTO:
    name: str
    player1_id: str
    player2_id: str
    status: str = "ACTIVE"
    tournaments_disputed: int = 0
    titles_won: int = 0


@dataclass
class PairResponseDTO:
    id: str
    name: str
    status: str
    player1_id: str
    player2_id: str
    player1_name: str
    player2_name: str
    player1_avatar: str
    player2_avatar: str
    tournaments_disputed: int
    titles_won: int
    created_at: str
