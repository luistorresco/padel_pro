from enum import Enum


class CourtStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"
    INACTIVE = "INACTIVE"

    @classmethod
    def normalize(cls, value: str | None) -> "CourtStatus":
        if not value:
            return cls.AVAILABLE
        v = str(value).strip().upper()
        try:
            return cls(v)
        except ValueError:
            return cls.AVAILABLE
