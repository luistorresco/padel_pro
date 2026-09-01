"""Courts use cases."""

from domain.exceptions import EntityNotFound


class ListCourtsUseCase:
    def __init__(self, court_repo):
        self.court_repo = court_repo

    def execute(self):
        courts = self.court_repo.list_all()
        return [
            {
                "id": c.id,
                "business_id": c.business_id,
                "name": c.name,
                "location": c.location,
                "number": c.number,
                "status": c.status,
                "created_at": c.created_at,
                "updated_at": c.updated_at,
            }
            for c in courts
        ]


class GetCourtUseCase:
    def __init__(self, court_repo):
        self.court_repo = court_repo

    def execute(self, court_id):
        c = self.court_repo.find_by_id(court_id)
        if not c:
            raise EntityNotFound("Court not found")
        return {
            "id": c.id,
            "business_id": c.business_id,
            "name": c.name,
            "location": c.location,
            "number": c.number,
            "status": c.status,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }


class CreateCourtUseCase:
    def __init__(self, court_repo):
        self.court_repo = court_repo

    def execute(self, court_data):
        from domain.entities.court import Court
        c = Court(
            court_id=court_data["id"],
            name=court_data["name"],
            business_id=court_data.get("business_id"),
            status=court_data.get("status", "AVAILABLE"),
            location=court_data.get("location"),
            number=court_data.get("number"),
        )
        saved = self.court_repo.save(c)
        return court_data


class UpdateCourtUseCase:
    def __init__(self, court_repo):
        self.court_repo = court_repo

    def execute(self, court_id, court_data):
        c = self.court_repo.find_by_id(court_id)
        if not c:
            raise EntityNotFound("Court not found")
        from domain.entities.court import Court
        updated = Court(
            court_id=court_id,
            name=court_data.get("name", c.name),
            business_id=court_data.get("business_id", c.business_id),
            status=court_data.get("status", c.status),
            location=court_data.get("location", c.location),
            number=court_data.get("number", c.number),
        )
        saved = self.court_repo.save(updated)
        return {"id": court_id, **court_data}


class DeleteCourtUseCase:
    def __init__(self, court_repo):
        self.court_repo = court_repo

    def execute(self, court_id):
        c = self.court_repo.find_by_id(court_id)
        if not c:
            raise EntityNotFound("Court not found")
        self.court_repo.delete(court_id)
        return {"message": "Court deleted"}
