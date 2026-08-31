"""Match event entity."""


class MatchEvent:
    def __init__(
        self,
        event_id: str,
        match_id: str,
        event_type: str,
        set_number: int,
        timestamp: str,
        game_number: int | None = None,
        winning_pair_id: str | None = None,
        player_id: str | None = None,
        description: str | None = None,
        score_snapshot: dict | None = None,
    ):
        self.id = event_id
        self.match_id = match_id
        self.event_type = event_type
        self.set_number = set_number
        self.timestamp = timestamp
        self.game_number = game_number
        self.winning_pair_id = winning_pair_id
        self.player_id = player_id
        self.description = description
        self.score_snapshot = score_snapshot
