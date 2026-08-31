"""Dominant hand value object."""

from domain.exceptions import ValidationError


class DominantHand:
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    BOTH = "BOTH"

    MAPPING = {
        "derecha": RIGHT,
        "right": RIGHT,
        "d": RIGHT,
        "r": RIGHT,
        "drive (derecha)": RIGHT,
        "revés (izquierda)": LEFT,
        "reves (izquierda)": LEFT,
        "zurda": LEFT,
        "left": LEFT,
        "z": LEFT,
        "l": LEFT,
        "ambas": BOTH,
        "both": BOTH,
        "a": BOTH,
        "b": BOTH,
    }

    @classmethod
    def from_string(cls, value: str | None) -> str | None:
        if not value:
            return None
        return cls.MAPPING.get(value.strip().lower())
