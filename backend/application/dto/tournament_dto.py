"""Tournament DTOs."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TournamentCreateDTO:
    name: str
    created_by: str
    start_date: str
    business_id: str | None = None
    logo: str | None = None
    description: str | None = None
    category: str | None = None
    level: str | None = None
    location: str | None = None
    end_date: str | None = None
    format: str | None = None
    max_pairs: int | None = None
    visibility: str = "PRIVATE"
    rules: dict | None = None


@dataclass
class TournamentResponseDTO:
    id: str
    name: str
    created_by: str
    start_date: str
    status: str
    business_id: str | None
    logo: str | None
    description: str | None
    category: str | None
    level: str | None
    location: str | None
    end_date: str | None
    format: str | None
    max_pairs: int | None
    visibility: str
    rules: dict
    created_at: str | None
    updated_at: str | None
    deleted_at: str | None
