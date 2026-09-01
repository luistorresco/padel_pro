"""Court entity."""


class Court:
    def __init__(
        self,
        court_id: str,
        name: str,
        business_id: str,
        status: str = "AVAILABLE",
        location: str | None = None,
        number: int | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
    ):
        self.id = court_id
        self.name = name
        self.business_id = business_id
        self.status = status
        self.location = location
        self.number = number
        self.created_at = created_at
        self.updated_at = updated_at
