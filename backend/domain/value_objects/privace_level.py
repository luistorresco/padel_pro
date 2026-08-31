from enum import Enum


class PrivacyLevel(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    @classmethod
    def default(cls) -> "PrivacyLevel":
        return cls.PUBLIC
