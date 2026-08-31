"""User points entity."""


class UserPoints:
    def __init__(
        self,
        user_id: str,
        points: int,
        match_id: str | None = None,
        tournament_id: str | None = None,
        reason: str | None = None,
    ):
        self.user_id = user_id
        self.match_id = match_id
        self.tournament_id = tournament_id
        self.points = points
        self.reason = reason
