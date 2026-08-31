"""Stats service - stats aggregation and defaults."""

from domain.value_objects.stats import PlayerStats


class StatsService:
    @staticmethod
    def default_stats() -> dict:
        return PlayerStats().to_dict()

    @staticmethod
    def normalize_stats(raw: dict | None) -> dict:
        if not raw:
            return PlayerStats().to_dict()
        if isinstance(raw, str):
            try:
                import json
                raw = json.loads(raw)
            except Exception:
                raw = {}
        stats = PlayerStats.from_dict(raw)
        return stats.to_dict()

    @staticmethod
    def add_match_stats(stats: dict, won: bool) -> dict:
        stats["matches_played"] = stats.get("matches_played", 0) + 1
        if won:
            stats["matches_won"] = stats.get("matches_won", 0) + 1
        else:
            stats["matches_lost"] = stats.get("matches_lost", 0) + 1
        return stats
