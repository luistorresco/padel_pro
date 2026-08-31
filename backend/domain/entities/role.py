"""Role entity."""


class Role:
    def __init__(self, role_id: int, name: str, description: str | None = None):
        self.id = role_id
        self.name = name
        self.description = description
