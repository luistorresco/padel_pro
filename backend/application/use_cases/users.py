"""Users use cases."""

from domain.exceptions import EntityNotFound, ValidationError


class ListUsersUseCase:
    def __init__(self, user_repo, privacy_service):
        self.user_repo = user_repo
        self.privacy_service = privacy_service

    def execute(self):
        users = self.user_repo.list_all(limit=1000)
        result = []
        for user in users:
            role = self.user_repo.find_role_by_user(user.id) or "PLAYER"
            privacy = self.user_repo.find_privacy(user.id)
            from domain.value_objects.privacy_settings import PrivacySettings
            pv = PrivacySettings(
                user_id=user.id,
                profile_visibility=privacy.get("profile_visibility", "PUBLIC"),
                points_visibility=privacy.get("points_visibility", "PUBLIC"),
                games_visibility=privacy.get("games_visibility", "PUBLIC"),
                tournaments_visibility=privacy.get("tournaments_visibility", "PUBLIC"),
            )
            level = user.level or "Intermedio"
            position = user.position or "Drive (Derecha)"
            dominant_hand = user.dominant_hand or "Derecha"
            resp = {
                "id": user.id,
                "name": user.name or "",
                "surname": user.surname or "",
                "username": user.username or "",
                "email": user.email or "",
                "avatar": user.avatar or "",
                "level": level,
                "position": position,
                "dominant_hand": dominant_hand,
                "points": user.points or 0,
                "stats": {},
                "role": role,
                "account_type": user.account_type or "USER",
                "status": user.status or "ACTIVE",
                "invitation_code": user.invitation_code,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "phone": None,
                "current_pair_id": None,
                "partner_name": None,
            }
            result.append(self.privacy_service.apply_user_privacy(resp, pv, viewer_is_self=False))
        return result


class GetUserUseCase:
    def __init__(self, user_repo, privacy_service):
        self.user_repo = user_repo
        self.privacy_service = privacy_service

    def execute(self, user_id):
        user = self.user_repo.find_with_role(user_id)
        if not user:
            raise EntityNotFound("User not found")
        privacy = self.user_repo.find_privacy(user_id)
        from domain.value_objects.privacy_settings import PrivacySettings
        pv = PrivacySettings(
            user_id=user_id,
            profile_visibility=privacy.get("profile_visibility", "PUBLIC"),
            points_visibility=privacy.get("points_visibility", "PUBLIC"),
            games_visibility=privacy.get("games_visibility", "PUBLIC"),
            tournaments_visibility=privacy.get("tournaments_visibility", "PUBLIC"),
        )
        level = user.get("level") or "Intermedio"
        position = user.get("position") or "Drive (Derecha)"
        dominant_hand = user.get("dominant_hand") or "Derecha"
        resp = {
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
            "stats": {},
            "role": user.get("role_name") or "PLAYER",
            "account_type": user.get("account_type") or "USER",
            "status": user.get("status") or "ACTIVE",
            "invitation_code": user.get("invitation_code"),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
            "phone": None,
            "current_pair_id": None,
            "partner_name": None,
        }
        return self.privacy_service.apply_user_privacy(resp, pv, viewer_is_self=False)


class CreateUserUseCase:
    def __init__(self, user_repo, auth_service):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, user_data):
        from domain.entities.user import User
        user = User(
            user_id=user_data["id"],
            name=user_data["name"],
            surname=user_data.get("surname", ""),
            username=user_data["username"],
            email=user_data.get("email"),
            avatar=user_data.get("avatar"),
            account_type="USER",
            status="ACTIVE",
            level=user_data.get("level"),
            position=user_data.get("position"),
            dominant_hand=user_data.get("dominant_hand"),
            points=user_data.get("points", 0),
        )
        self.user_repo.save(user)
        if user_data.get("email"):
            hashed = self.auth_service.hash_password(user_data.get("password") or "password")
            self.user_repo.create_auth(user["id"], user_data["email"], hashed)
        return user_data


class UpdateUserUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, user_id, user_data):
        from domain.entities.user import User
        existing = self.user_repo.find_by_id(user_id)
        if not existing:
            raise EntityNotFound("User not found")
        updated = User(
            user_id=user_id,
            name=user_data.get("name", existing.name),
            surname=user_data.get("surname", existing.surname),
            username=user_data.get("username", existing.username),
            email=user_data.get("email", existing.email),
            avatar=user_data.get("avatar", existing.avatar),
            account_type=existing.account_type,
            status=existing.status,
            level=user_data.get("level", existing.level),
            position=user_data.get("position", existing.position),
            dominant_hand=user_data.get("dominant_hand", existing.dominant_hand),
            points=user_data.get("points", existing.points),
            invited_by=existing.invited_by,
            invitation_code=existing.invitation_code,
            converted_at=existing.converted_at,
            deleted_at=existing.deleted_at,
        )
        self.user_repo.save(updated)
        return {"id": user_id, **user_data}


class DeleteUserUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, user_id):
        existing = self.user_repo.find_by_id(user_id)
        if not existing:
            raise EntityNotFound("User not found")
        try:
            self.user_repo.delete(user_id)
            return {"message": "User soft-deleted"}
        except Exception:
            self.user_repo.hard_delete(user_id)
            return {"message": "User deleted"}
