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
    ):
        self.id = court_id
        self.name = name
        self.business_id = business_id
        self.status = status
        self.location = location
        self.number = number
