"""User DTOs."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserCreateDTO:
    name: str
    email: str
    password: str
    surname: str = ""
    username: str = ""
    role: str = "PLAYER"
    avatar: str | None = None
    level: str | None = None
    position: str | None = None
    dominant_hand: str | None = None
    points: int = 0


@dataclass
class UserUpdateDTO:
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    email: str | None = None
    avatar: str | None = None
    level: str | None = None
    position: str | None = None
    dominant_hand: str | None = None
    points: int | None = None


@dataclass
class UserResponseDTO:
    id: str
    name: str
    surname: str
    username: str
    email: str
    avatar: str
    level: str
    position: str
    dominant_hand: str
    points: int
    stats: dict
    role: str
    account_type: str
    status: str
    invitation_code: str | None
    created_at: str | None
    updated_at: str | None
    phone: str | None
    current_pair_id: str | None
    partner_name: str | None
