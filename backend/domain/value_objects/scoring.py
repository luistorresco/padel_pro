"""Padel scoring value objects."""

POINT_SEQUENCE = ["0", "15", "30", "40"]


def next_point(current: str) -> str:
    idx = POINT_SEQUENCE.index(current) if current in POINT_SEQUENCE else -1
    if idx + 1 < len(POINT_SEQUENCE):
        return POINT_SEQUENCE[idx + 1]
    return current


def is_deuce(team_a: str, team_b: str) -> bool:
    return team_a == "40" and team_b == "40"


def has_advantage(team_a: str, team_b: str) -> str | None:
    if team_a == "AD" and team_b != "AD":
        return "A"
    if team_b == "AD" and team_a != "AD":
        return "B"
    return None
