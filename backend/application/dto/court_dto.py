"""Court DTOs."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CourtCreateDTO:
    name: str
    business_id: str
    location: str | None = None
    number: int | None = None
    status: str = "AVAILABLE"


@dataclass
class CourtResponseDTO:
    id: str
    name: str
    business_id: str
    location: str | None
    number: int | None
    status: str
    created_at: str | None
    updated_at: str | None
