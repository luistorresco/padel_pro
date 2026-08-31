from typing import Dict, Any, List

from domain.services.privacy_service import PrivacyService
from domain.services.tournament_rules_service import TournamentRulesService
from domain.services.stats_service import StatsService


class UserResponseBuilder:
    @staticmethod
    def build(user: Dict[str, Any], role_name: str = None) -> Dict[str, Any]:
        level = user.get("level") or "Intermedio"
        position = user.get("position") or "Drive (Derecha)"
        dominant_hand = user.get("dominant_hand") or "Derecha"
        stats = user.get("stats")
        if not stats:
            stats = {}
        if isinstance(stats, str):
            import json
            try:
                stats = json.loads(stats)
            except Exception:
                stats = {}
        stats = StatsService.normalize_stats(stats) if not isinstance(stats, dict) or not stats else stats
        if not isinstance(stats, dict):
            stats = {}
        return {
            "id": user.get("id"),
            "name": user.get("name") or "",
            "surname": user.get("surname") or "",
            "username": user.get("username") or "",
            "email": user.get("email") or "",
            "avatar": user.get("avatar") or "",
            "level": level,
            "position": position,
            "dominant_hand": dominant_hand,
            "points": user.get("points") or 0,
            "stats": stats,
            "role": role_name or "PLAYER",
            "account_type": user.get("account_type") or "USER",
            "status": user.get("status") or "ACTIVE",
            "invitation_code": user.get("invitation_code"),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
            "phone": None,
            "current_pair_id": None,
            "partner_name": None,
        }


class TournamentResponseBuilder:
    @staticmethod
    def build(t: Dict[str, Any]) -> Dict[str, Any]:
        rules = TournamentRulesService.normalize_rules(t.get("rules"))
        return {
            "id": t.get("id"),
            "name": t.get("name") or "",
            "logo": t.get("logo") or "🏆",
            "description": t.get("description") or "",
            "category": t.get("category") or "Masculino",
            "level": t.get("level") or "Intermedio",
            "location": t.get("location") or "",
            "start_date": t.get("start_date"),
            "end_date": t.get("end_date"),
            "status": t.get("status") or "DRAFT",
            "format": t.get("format") or "Eliminación directa",
            "max_pairs": t.get("max_pairs") or 0,
            "visibility": t.get("visibility") or "PRIVATE",
            "rules": rules,
            "registered_pair_ids": t.get("registered_pair_ids", []),
            "registered_user_ids": t.get("registered_user_ids", []),
            "court_ids": t.get("court_ids", []),
            "business_id": t.get("business_id"),
            "created_by": t.get("created_by"),
            "created_at": t.get("created_at"),
            "updated_at": t.get("updated_at"),
            "deleted_at": t.get("deleted_at"),
        }


class PairResponseBuilder:
    @staticmethod
    def build_simple(r: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": r["id"],
            "name": r["name"],
            "status": r["status"],
            "player1Id": r["player1_id"],
            "player2Id": r["player2_id"],
            "player1Name": f"{r['player1_name']} {r['player1_surname'] or ''}".strip(),
            "player2Name": f"{r['player2_name']} {r['player2_surname'] or ''}".strip(),
            "player1Avatar": r["player1_avatar"] or "",
            "player2Avatar": r["player2_avatar"] or "",
            "createdAt": r["created_at"],
            "tournamentsDisputed": r["tournaments_disputed"],
            "titlesWon": r["titles_won"],
        }

    @staticmethod
    def build_enriched(enriched: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": enriched["id"],
            "name": enriched["name"],
            "status": enriched["status"],
            "player1Id": enriched["player1_id"],
            "player2Id": enriched["player2_id"],
            "player1Name": f"{enriched['p1_name']} {enriched['p1_surname'] or ''}".strip(),
            "player2Name": f"{enriched['p2_name']} {enriched['p2_surname'] or ''}".strip(),
            "player1Avatar": enriched["p1_avatar"] or "",
            "player2Avatar": enriched["p2_avatar"] or "",
            "p1Level": enriched["p1_level"],
            "p2Level": enriched["p2_level"],
            "p1Points": enriched["p1_points"],
            "p2Points": enriched["p2_points"],
            "tournamentsDisputed": enriched["tournaments_disputed"],
            "titlesWon": enriched["titles_won"],
        }


class MatchResponseBuilder:
    @staticmethod
    def build_list(matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        import json
        result = []
        for m in matches:
            mm = dict(m)
            if isinstance(mm.get("sets"), str):
                mm["sets"] = json.loads(mm["sets"])
            mm.setdefault("roundId", None)
            mm.setdefault("businessId", None)
            mm.setdefault("visibility", "PRIVATE")
            mm.setdefault("currentSetIndex", 0)
            mm.setdefault("winnerPairId", None)
            mm.setdefault("winnerTeam", None)
            mm.setdefault("startTimeMs", None)
            mm.setdefault("elapsedTimeSec", 0)
            mm.setdefault("goldenPoint", 0)
            mm.setdefault("setsToWin", 2)
            mm.setdefault("roundName", None)
            mm.setdefault("deletedAt", None)
            mm.setdefault("playerA1Name", mm.get("playerA1Name") or "Jugador 1")
            mm.setdefault("playerA2Name", mm.get("playerA2Name") or "Jugador 2")
            mm.setdefault("playerB1Name", mm.get("playerB1Name") or "Jugador 3")
            mm.setdefault("playerB2Name", mm.get("playerB2Name") or "Jugador 4")
            mm.setdefault("playerA1Avatar", mm.get("playerA1Avatar") or "")
            mm.setdefault("playerA2Avatar", mm.get("playerA2Avatar") or "")
            mm.setdefault("playerB1Avatar", mm.get("playerB1Avatar") or "")
            mm.setdefault("playerB2Avatar", mm.get("playerB2Avatar") or "")
            mm.setdefault("pairAName", mm.get("pairAName") or "Pareja A")
            mm.setdefault("pairBName", mm.get("pairBName") or "Pareja B")
            mm.setdefault("courtName", mm.get("courtName") or "Pista por definir")
            mm["current_game"] = {}
            result.append(mm)
        return result
