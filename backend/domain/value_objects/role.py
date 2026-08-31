from enum import Enum


class Role(str, Enum):
    PLAYER = "PLAYER"
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    BUSINESS_ADMIN = "BUSINESS_ADMIN"
    BUSINESS_MANAGER = "BUSINESS_MANAGER"

    @property
    def is_admin(self) -> bool:
        return self.value in {
            Role.ADMIN.value,
            Role.SUPER_ADMIN.value,
            Role.BUSINESS_ADMIN.value,
            Role.BUSINESS_MANAGER.value,
        }

    @classmethod
    def from_token(cls, role_str: str | None) -> "Role":
        if not role_str:
            return cls.PLAYER
        try:
            return cls(role_str.upper())
        except ValueError:
            return cls.PLAYER

    @classmethod
    def map_from_raw(cls, raw_role: str | None) -> str:
        mapping = {
            "ADMIN": "SUPER_ADMIN",
            "SUPER_ADMIN": "SUPER_ADMIN",
            "BUSINESS_ADMIN": "BUSINESS_ADMIN",
            "BUSINESS_MANAGER": "BUSINESS_MANAGER",
            "MANAGER": "BUSINESS_MANAGER",
            "USER": "USER",
            "PLAYER": "USER",
        }
        return mapping.get(raw_role or "USER", "USER")


ADMIN_ROLES = {Role.ADMIN.value, Role.SUPER_ADMIN.value, Role.BUSINESS_ADMIN.value, Role.BUSINESS_MANAGER.value}
