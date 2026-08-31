import re

_CAMEL_TO_SNAKE_MATCH = {
    "tournamentId": "tournament_id",
    "tournamentName": "tournament_name",
    "courtId": "court_id",
    "courtName": "court_name",
    "dateTime": "date_time",
    "pairAId": "pair_a_id",
    "pairBId": "pair_b_id",
    "pairAName": "pair_a_name",
    "pairBName": "pair_b_name",
    "playerA1Id": "player_a1_id",
    "playerA2Id": "player_a2_id",
    "playerB1Id": "player_b1_id",
    "playerB2Id": "player_b2_id",
    "playerA1Name": "player_a1_name",
    "playerA2Name": "player_a2_name",
    "playerB1Name": "player_b1_name",
    "playerB2Name": "player_b2_name",
    "playerA1Avatar": "player_a1_avatar",
    "playerA2Avatar": "player_a2_avatar",
    "playerB1Avatar": "player_b1_avatar",
    "playerB2Avatar": "player_b2_avatar",
    "currentGame": "current_game",
    "currentSetIndex": "current_set_index",
    "winnerPairId": "winner_pair_id",
    "winnerTeam": "winner_team",
    "startTimeMs": "start_time_ms",
    "elapsedTimeSec": "elapsed_time_sec",
    "goldenPoint": "golden_point",
    "setsToWin": "sets_to_win",
    "roundName": "round_name",
}

_CAMEL_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


def _camel_to_snake(key: str) -> str:
    return _CAMEL_PATTERN.sub("_", key).lower()


def normalize_match_payload(match: dict) -> dict:
    out = {}
    for key, value in match.items():
        snake = _CAMEL_TO_SNAKE_MATCH.get(key)
        if snake is None:
            snake = _camel_to_snake(key)
        out[snake] = value
    return out
