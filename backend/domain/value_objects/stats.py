"""Player stats value object."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlayerStats:
    points_won: int = 0
    winners: int = 0
    smashes: int = 0
    smashes_won: int = 0
    voleas_won: int = 0
    bandejas: int = 0
    viboras: int = 0
    remates: int = 0
    net_points_won: int = 0
    touches: int = 0
    shots: int = 0
    serves: int = 0
    first_serves: int = 0
    second_serves: int = 0
    aces: int = 0
    double_faults: int = 0
    break_points: int = 0
    break_points_won: int = 0
    recoveries: int = 0
    globos: int = 0
    devoluciones: int = 0
    points_saved: int = 0
    unforced_errors: int = 0
    distance_km: float = 0.0
    time_played_min: int = 0
    avg_speed_kmh: float = 0.0
    moves_count: int = 0
    matches_played: int = 0
    matches_won: int = 0
    matches_lost: int = 0
    sets_won: int = 0
    sets_lost: int = 0
    games_won: int = 0
    games_lost: int = 0

    @classmethod
    def from_dict(cls, data: dict | None) -> "PlayerStats":
        if not data:
            return cls()
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict[str, Any]:
        return {
            "points_won": self.points_won,
            "winners": self.winners,
            "smashes": self.smashes,
            "smashes_won": self.smashes_won,
            "voleas_won": self.voleas_won,
            "bandejas": self.bandejas,
            "viboras": self.viboras,
            "remates": self.remates,
            "net_points_won": self.net_points_won,
            "touches": self.touches,
            "shots": self.shots,
            "serves": self.serves,
            "first_serves": self.first_serves,
            "second_serves": self.second_serves,
            "aces": self.aces,
            "double_faults": self.double_faults,
            "break_points": self.break_points,
            "break_points_won": self.break_points_won,
            "recoveries": self.recoveries,
            "globos": self.globos,
            "devoluciones": self.devoluciones,
            "points_saved": self.points_saved,
            "unforced_errors": self.unforced_errors,
            "distance_km": self.distance_km,
            "time_played_min": self.time_played_min,
            "avg_speed_kmh": self.avg_speed_kmh,
            "moves_count": self.moves_count,
            "matches_played": self.matches_played,
            "matches_won": self.matches_won,
            "matches_lost": self.matches_lost,
            "sets_won": self.sets_won,
            "sets_lost": self.sets_lost,
            "games_won": self.games_won,
            "games_lost": self.games_lost,
        }
