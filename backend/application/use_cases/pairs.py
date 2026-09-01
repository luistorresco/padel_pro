"""Pairs use cases."""

from domain.exceptions import EntityNotFound


class ListPairsUseCase:
    def __init__(self, pair_repo):
        self.pair_repo = pair_repo

    def execute(self):
        pairs = self.pair_repo.list_all()
        result = []
        for p in pairs:
            detailed = self.pair_repo.find_with_players(p.id)
            if detailed:
                result.append({
                    "id": p.id,
                    "name": p.name,
                    "status": p.status,
                    "player1Id": p.player1_id,
                    "player2Id": p.player2_id,
                    "player1Name": detailed.get("player1_name") or "",
                    "player2Name": detailed.get("player2_name") or "",
                    "player1Avatar": detailed.get("player1_avatar") or "",
                    "player2Avatar": detailed.get("player2_avatar") or "",
                    "p1Level": detailed.get("p1_level") or "Intermedio",
                    "p2Level": detailed.get("p2_level") or "Intermedio",
                    "p1Points": detailed.get("p1_points") or 0,
                    "p2Points": detailed.get("p2_points") or 0,
                    "tournamentsDisputed": p.tournaments_disputed,
                    "titlesWon": p.titles_won,
                    "createdAt": getattr(p, 'created_at', None),
                })
            else:
                result.append({
                    "id": p.id,
                    "name": p.name,
                    "status": p.status,
                    "player1Id": p.player1_id,
                    "player2Id": p.player2_id,
                    "player1Name": "",
                    "player2Name": "",
                    "player1Avatar": "",
                    "player2Avatar": "",
                    "p1Level": "Intermedio",
                    "p2Level": "Intermedio",
                    "p1Points": 0,
                    "p2Points": 0,
                    "tournamentsDisputed": p.tournaments_disputed,
                    "titlesWon": p.titles_won,
                    "createdAt": getattr(p, 'created_at', None),
                })
        return result


class GetPairUseCase:
    def __init__(self, pair_repo):
        self.pair_repo = pair_repo

    def execute(self, pair_id):
        p = self.pair_repo.find_by_id(pair_id)
        if not p:
            raise EntityNotFound("Pair not found")
        detailed = self.pair_repo.find_with_players(pair_id)
        if not detailed:
            detailed = {}
        return {
            "id": p.id,
            "name": p.name,
            "status": p.status,
            "player1Id": p.player1_id,
            "player2Id": p.player2_id,
            "player1Name": detailed.get("player1_name") or "",
            "player2Name": detailed.get("player2_name") or "",
            "player1Avatar": detailed.get("player1_avatar") or "",
            "player2Avatar": detailed.get("player2_avatar") or "",
            "p1Level": detailed.get("p1_level") or "Intermedio",
            "p2Level": detailed.get("p2_level") or "Intermedio",
            "p1Points": detailed.get("p1_points") or 0,
            "p2Points": detailed.get("p2_points") or 0,
            "tournamentsDisputed": p.tournaments_disputed,
            "titlesWon": p.titles_won,
            "createdAt": getattr(p, 'created_at', None),
        }


class CreatePairUseCase:
    def __init__(self, pair_repo):
        self.pair_repo = pair_repo

    def execute(self, pair_data):
        from domain.entities.pair import Pair
        p = Pair(
            pair_id=pair_data.get("id") or pair_data.get("player1Id") + "_" + pair_data.get("player2Id"),
            name=pair_data.get("name"),
            player1_id=pair_data.get("player1Id") or pair_data.get("player1_id"),
            player2_id=pair_data.get("player2Id") or pair_data.get("player2_id"),
            created_by=pair_data.get("createdBy") or pair_data.get("created_by") or pair_data.get("player1Id") or pair_data.get("player1_id"),
            status=pair_data.get("status", "ACTIVE"),
            tournaments_disputed=pair_data.get("tournamentsDisputed", pair_data.get("tournaments_disputed", 0)),
            titles_won=pair_data.get("titlesWon", pair_data.get("titles_won", 0)),
        )
        saved = self.pair_repo.save(p)
        return pair_data


class DeletePairUseCase:
    def __init__(self, pair_repo):
        self.pair_repo = pair_repo

    def execute(self, pair_id):
        p = self.pair_repo.find_by_id(pair_id)
        if not p:
            raise EntityNotFound("Pair not found")
        self.pair_repo.delete(pair_id)
        return {"message": "Pair deleted"}
