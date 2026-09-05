"""Tournaments use cases."""

from domain.exceptions import EntityNotFound


def _normalize_tournament_status(status: str | None) -> str:
    if not status:
        return "UPCOMING"
    s = str(status).strip().upper()
    if s == "IN_PROGRESS":
        return "ACTIVE"
    if s == "OPEN":
        return "REGISTRATION"
    if s == "DRAFT":
        return "UPCOMING"
    return s


class ListTournamentsUseCase:
    def __init__(self, tournament_repo, match_repo):
        self.tournament_repo = tournament_repo
        self.match_repo = match_repo

    def execute(self):
        tournaments = self.tournament_repo.list_all()
        result = []
        for t in tournaments:
            pairs = self.tournament_repo.find_full(t.id)
            registered_pair_ids = []
            registered_user_ids = []
            court_ids = []
            if pairs:
                for p in pairs.get("pairs", []):
                    registered_pair_ids.append(p.get("pair_id") or p.get("id"))
                for p in pairs.get("players", []):
                    registered_user_ids.append(p.get("user_id"))
                for m in pairs.get("matches", []):
                    if m.get("courtId") or m.get("court_id"):
                        court_ids.append(m.get("courtId") or m.get("court_id"))
            result.append({
                "id": t.id,
                "name": t.name,
                "created_by": t.created_by,
                "start_date": t.start_date,
                "end_date": t.end_date,
                "status": _normalize_tournament_status(t.status),
                "business_id": t.business_id,
                "logo": t.logo,
                "description": t.description,
                "category": t.category,
                "level": t.level,
                "location": t.location,
                "format": t.format,
                "max_pairs": t.max_pairs,
                "visibility": t.visibility,
                "rules": t.rules or {},
                "created_at": getattr(t, 'created_at', None),
                "updated_at": getattr(t, 'updated_at', None),
                "deleted_at": t.deleted_at,
                "registeredPairIds": registered_pair_ids,
                "registeredUserIds": registered_user_ids,
                "courtIds": court_ids,
            })
        return result


class GetTournamentUseCase:
    def __init__(self, tournament_repo, match_repo):
        self.tournament_repo = tournament_repo
        self.match_repo = match_repo

    def execute(self, tournament_id):
        t = self.tournament_repo.find_by_id(tournament_id)
        if not t:
            raise EntityNotFound("Tournament not found")
        full = self.tournament_repo.find_full(tournament_id)
        registered_pair_ids = []
        registered_user_ids = []
        court_ids = []
        if full:
            for p in full.get("pairs", []):
                registered_pair_ids.append(p.get("pair_id") or p.get("id"))
            for p in full.get("players", []):
                registered_user_ids.append(p.get("user_id"))
            for m in full.get("matches", []):
                if m.get("courtId") or m.get("court_id"):
                    court_ids.append(m.get("courtId") or m.get("court_id"))
        return {
            "id": t.id,
            "name": t.name,
            "created_by": t.created_by,
            "start_date": t.start_date,
            "end_date": t.end_date,
            "status": _normalize_tournament_status(t.status),
            "business_id": t.business_id,
            "logo": t.logo,
            "description": t.description,
            "category": t.category,
            "level": t.level,
            "location": t.location,
            "format": t.format,
            "max_pairs": t.max_pairs,
            "visibility": t.visibility,
            "rules": t.rules or {},
            "created_at": getattr(t, 'created_at', None),
            "updated_at": getattr(t, 'updated_at', None),
            "deleted_at": t.deleted_at,
            "registeredPairIds": registered_pair_ids,
            "registeredUserIds": registered_user_ids,
            "courtIds": court_ids,
        }


class GetTournamentFullUseCase:
    def __init__(self, tournament_repo):
        self.tournament_repo = tournament_repo

    def execute(self, tournament_id):
        data = self.tournament_repo.find_full(tournament_id)
        if not data:
            raise EntityNotFound("Tournament not found")
        t = data["tournament"]
        base = {
            "id": t.tournament_id,
            "name": t.name,
            "created_by": t.created_by,
            "start_date": t.start_date,
            "end_date": t.end_date,
            "status": _normalize_tournament_status(t.status),
            "business_id": t.business_id,
            "logo": t.logo,
            "description": t.description,
            "category": t.category,
            "level": t.level,
            "location": t.location,
            "format": t.format,
            "max_pairs": t.max_pairs,
            "visibility": t.visibility,
            "rules": t.rules or {},
            "created_at": getattr(t, 'created_at', None),
            "updated_at": getattr(t, 'updated_at', None),
            "deleted_at": t.deleted_at,
        }
        return {
            **base,
            "categories": [dict(c) for c in data["categories"]],
            "rounds": [dict(r) for r in data["rounds"]],
            "pairs": [dict(p) for p in data["pairs"]],
            "players": [dict(p) for p in data["players"]],
            "matches": [dict(m) for m in data["matches"]],
        }


class CreateTournamentUseCase:
    def __init__(self, tournament_repo):
        self.tournament_repo = tournament_repo

    def execute(self, tournament_data):
        from domain.entities.tournament import Tournament
        t = Tournament(
            tournament_id=tournament_data["id"],
            name=tournament_data["name"],
            created_by=tournament_data.get("created_by", ""),
            start_date=tournament_data.get("start_date"),
            end_date=tournament_data.get("end_date"),
            status=tournament_data.get("status", "DRAFT"),
            business_id=tournament_data.get("business_id"),
            logo=tournament_data.get("logo"),
            description=tournament_data.get("description"),
            category=tournament_data.get("category"),
            level=tournament_data.get("level"),
            location=tournament_data.get("location"),
            format=tournament_data.get("format"),
            max_pairs=tournament_data.get("max_pairs"),
            visibility=tournament_data.get("visibility", "PRIVATE"),
            rules=tournament_data.get("rules") or {},
        )
        saved = self.tournament_repo.save(t)
        return {**tournament_data, "id": saved.id}


class UpdateTournamentUseCase:
    def __init__(self, tournament_repo):
        self.tournament_repo = tournament_repo

    def execute(self, tournament_id, tournament_data):
        t = self.tournament_repo.find_by_id(tournament_id)
        if not t:
            raise EntityNotFound("Tournament not found")
        from domain.entities.tournament import Tournament
        updated = Tournament(
            tournament_id=tournament_id,
            name=tournament_data.get("name", t.name),
            created_by=t.created_by,
            start_date=tournament_data.get("start_date", t.start_date),
            end_date=tournament_data.get("end_date", t.end_date),
            status=tournament_data.get("status", t.status),
            business_id=tournament_data.get("business_id", t.business_id),
            logo=tournament_data.get("logo", t.logo),
            description=tournament_data.get("description", t.description),
            category=tournament_data.get("category", t.category),
            level=tournament_data.get("level", t.level),
            location=tournament_data.get("location", t.location),
            format=tournament_data.get("format", t.format),
            max_pairs=tournament_data.get("max_pairs", t.max_pairs),
            visibility=tournament_data.get("visibility", t.visibility),
            rules=tournament_data.get("rules") or t.rules,
        )
        saved = self.tournament_repo.save(updated)
        return {**tournament_data, "id": saved.id}


class DeleteTournamentUseCase:
    def __init__(self, tournament_repo, match_repo):
        self.tournament_repo = tournament_repo
        self.match_repo = match_repo

    def execute(self, tournament_id):
        t = self.tournament_repo.find_by_id(tournament_id)
        if not t:
            raise EntityNotFound("Tournament not found")
        matches = self.match_repo.find_by_tournament(tournament_id)
        for m in matches:
            self.match_repo.delete(m.id)
        self.tournament_repo.delete(tournament_id)
        return {"message": "Tournament deleted"}


class RegisterForTournamentUseCase:
    def __init__(self, tournament_repo, match_repo):
        self.tournament_repo = tournament_repo
        self.match_repo = match_repo

    def execute(self, tournament_id, body, created_by):
        t = self.tournament_repo.find_by_id(tournament_id)
        if not t:
            raise EntityNotFound("Tournament not found")

        pair_id = body.get("pairId") or body.get("pair_id")
        user_id = body.get("userId") or body.get("user_id")
        court_id = body.get("courtId") or body.get("court_id")
        date_time = body.get("dateTime") or body.get("date_time")
        if date_time:
            date_time = str(date_time).replace("T", " ").replace("Z", "")
            if len(date_time) == 16:
                date_time = date_time + ":00"

        if pair_id:
            self.tournament_repo.register_pair(tournament_id, pair_id)
        if user_id:
            self.tournament_repo.register_player(tournament_id, user_id)
        if pair_id and court_id and date_time:
            match_id = f"match_{tournament_id}_{pair_id}"
            from domain.entities.match import Match
            match = Match(
                match_id=match_id,
                tournament_id=tournament_id,
                pair_a_id=pair_id,
                court_id=court_id,
                date_time=date_time,
                status="SCHEDULED",
                created_by=created_by or "",
            )
            self.match_repo.save(match)
        return {"status": "registered"}
