from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    PRO = "PRO"

    @classmethod
    def normalize(cls, value: str | None) -> str | None:
        if not value:
            return None
        v = str(value).strip().lower()
        mapping = {
            "principiante": cls.BEGINNER,
            "intermedio": cls.INTERMEDIATE,
            "avanzado": cls.ADVANCED,
            "profesional": cls.PRO,
            "open": cls.PRO,
        }
        mapped = mapping.get(v)
        return mapped.value if mapped else None
