from enum import Enum


class TournamentStatus(str, Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"

    @classmethod
    def normalize(cls, value: str | None) -> "TournamentStatus":
        if not value:
            return cls.DRAFT
        v = str(value).strip().upper()
        if v == "REGISTRATION":
            return cls.OPEN
        if v == "ACTIVE":
            return cls.IN_PROGRESS
        if v == "UPCOMING":
            return cls.DRAFT
        try:
            return cls(v)
        except ValueError:
            return cls.DRAFT
