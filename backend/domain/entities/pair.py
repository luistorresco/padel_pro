"""Pair entity."""


class Pair:
    def __init__(
        self,
        pair_id: str,
        name: str,
        player1_id: str,
        player2_id: str,
        created_by: str,
        status: str = "ACTIVE",
        tournaments_disputed: int = 0,
        titles_won: int = 0,
    ):
        self.id = pair_id
        self.name = name
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.created_by = created_by
        self.status = status
        self.tournaments_disputed = tournaments_disputed
        self.titles_won = titles_won
