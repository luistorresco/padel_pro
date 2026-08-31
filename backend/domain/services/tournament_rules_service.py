from typing import Dict, Any


class TournamentRulesService:
    DEFAULT_POINTS_DISTRIBUTION = {
        "champion": 1000,
        "runnerUp": 600,
        "semiFinals": 360,
        "quarterFinals": 180,
        "groupStage": 90,
    }

    @staticmethod
    def normalize_rules(rules: Any) -> Dict[str, Any]:
        import json

        if isinstance(rules, str):
            try:
                rules = json.loads(rules)
            except Exception:
                rules = {}
        if not rules or not isinstance(rules, dict):
            rules = {}
        if "pointsDistribution" not in rules or not isinstance(rules.get("pointsDistribution"), dict):
            rules["pointsDistribution"] = dict(TournamentRulesService.DEFAULT_POINTS_DISTRIBUTION)
        if "goldenPoint" not in rules:
            rules["goldenPoint"] = False
        if "tieBreakAt" not in rules:
            rules["tieBreakAt"] = 6
        if "finalSetTieBreak" not in rules:
            rules["finalSetTieBreak"] = False
        if "setsToWin" not in rules:
            rules["setsToWin"] = 2
        return rules
