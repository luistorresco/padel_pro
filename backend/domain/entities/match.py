"""Match entity."""


class Match:
    def __init__(
        self,
        match_id: str,
        tournament_id: str | None,
        pair_a_id: str | None,
        pair_b_id: str | None,
        date_time: str | None,
        status: str = "SCHEDULED",
        court_id: str | None = None,
        round_id: str | None = None,
        business_id: str | None = None,
        created_by: str = "",
        visibility: str = "PRIVATE",
        sets: list | None = None,
        current_set_index: int = 0,
        winner_pair_id: str | None = None,
        winner_team: str | None = None,
        start_time_ms: int | None = None,
        elapsed_time_sec: int = 0,
        golden_point: bool = False,
        sets_to_win: int = 2,
        round_name: str | None = None,
        deleted_at: str | None = None,
    ):
        self.id = match_id
        self.tournament_id = tournament_id
        self.pair_a_id = pair_a_id
        self.pair_b_id = pair_b_id
        self.date_time = date_time
        self.status = status
        self.court_id = court_id
        self.round_id = round_id
        self.business_id = business_id
        self.created_by = created_by
        self.visibility = visibility
        self.sets = sets or []
        self.current_set_index = current_set_index
        self.winner_pair_id = winner_pair_id
        self.winner_team = winner_team
        self.start_time_ms = start_time_ms
        self.elapsed_time_sec = elapsed_time_sec
        self.golden_point = golden_point
        self.sets_to_win = sets_to_win
        self.round_name = round_name
        self.deleted_at = deleted_at
