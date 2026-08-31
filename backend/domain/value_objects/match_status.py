from enum import Enum


class MatchStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"

    @classmethod
    def normalize(cls, value: str | None) -> "MatchStatus":
        if not value:
            return cls.SCHEDULED
        v = str(value).strip().upper()
        if v == "LIVE":
            return cls.IN_PROGRESS
        if v == "UPCOMING":
            return cls.SCHEDULED
        try:
            return cls(v)
        except ValueError:
            return cls.SCHEDULED
