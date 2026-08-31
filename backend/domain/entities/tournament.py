"""Tournament entity."""


class Tournament:
    def __init__(
        self,
        tournament_id: str,
        name: str,
        created_by: str,
        start_date: str,
        status: str = "DRAFT",
        business_id: str | None = None,
        logo: str | None = None,
        description: str | None = None,
        category: str | None = None,
        level: str | None = None,
        location: str | None = None,
        end_date: str | None = None,
        format: str | None = None,
        max_pairs: int | None = None,
        visibility: str = "PRIVATE",
        rules: dict | None = None,
        deleted_at: str | None = None,
    ):
        self.id = tournament_id
        self.name = name
        self.created_by = created_by
        self.start_date = start_date
        self.status = status
        self.business_id = business_id
        self.logo = logo
        self.description = description
        self.category = category
        self.level = level
        self.location = location
        self.end_date = end_date
        self.format = format
        self.max_pairs = max_pairs
        self.visibility = visibility
        self.rules = rules or {}
        self.deleted_at = deleted_at
