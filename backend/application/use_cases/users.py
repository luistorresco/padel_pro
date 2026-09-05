"""Users use cases."""

from datetime import datetime
from domain.exceptions import EntityNotFound, ValidationError


class ListUsersUseCase:
    def __init__(self, user_repo, privacy_service):
        self.user_repo = user_repo
        self.privacy_service = privacy_service

    def execute(self, current_user_id: str | None = None, current_role: str | None = None):
        if current_role == "SUPER_ADMIN":
            users = self.user_repo.list_all(limit=1000)
        else:
            users = self.user_repo.list_by_inviter(current_user_id or "", limit=1000)
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
                "invited_by": user.invited_by,
                "converted_at": user.converted_at,
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
            "invited_by": user.get("invited_by"),
            "converted_at": user.get("converted_at"),
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

    def execute(self, user_data, created_by_role: str = "PLAYER"):
        if created_by_role != "SUPER_ADMIN":
            allowed_roles = {"PLAYER", "USER"}
            requested_role = user_data.get("role", "USER")
            if requested_role not in allowed_roles:
                raise ValidationError("Only super admin can create admin users")
        from domain.entities.user import User
        username = user_data.get("username") or (user_data.get("email") or "").split("@")[0] or f"user_{user_data['id']}"
        user = User(
            user_id=user_data["id"],
            name=user_data["name"],
            surname=user_data.get("surname", ""),
            username=username,
            email=user_data.get("email"),
            avatar=user_data.get("avatar"),
            account_type=user_data.get("account_type") or user_data.get("accountType", "USER"),
            status="ACTIVE",
            level=user_data.get("level"),
            position=user_data.get("position"),
            dominant_hand=user_data.get("dominant_hand"),
            points=user_data.get("points", 0),
            invited_by=user_data.get("invited_by") or user_data.get("invitedBy"),
            invitation_code=user_data.get("invitation_code") or user_data.get("invitationCode"),
            converted_at=user_data.get("converted_at") or user_data.get("convertedAt"),
        )
        self.user_repo.save(user)
        if user_data.get("email"):
            hashed = self.auth_service.hash_password(user_data.get("password") or "password")
            self.user_repo.create_auth(user.id, user_data["email"], hashed)
        if user_data.get("role"):
            self.user_repo.assign_role(user.id, user_data["role"])
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

    def execute(self, user_id, current_user_id: str, current_role: str):
        existing = self.user_repo.find_by_id(user_id)
        if not existing:
            raise EntityNotFound("User not found")
        if existing.invited_by and existing.converted_at:
            raise ValidationError("Cannot delete a converted user")
        if existing.id == current_user_id:
            raise ValidationError("Cannot delete yourself")
        if current_role != "SUPER_ADMIN":
            if existing.invited_by != current_user_id:
                raise ValidationError("You can only delete users you invited")
        try:
            self.user_repo.delete(user_id)
            return {"message": "User soft-deleted"}
        except Exception:
            self.user_repo.hard_delete(user_id)
            return {"message": "User deleted"}


class ConvertGuestUseCase:
    def __init__(self, user_repo, auth_service):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, invitation_code: str, password: str, user_data: dict):
        guest = self.user_repo.find_guest_by_invitation_code(invitation_code)
        if not guest:
            raise EntityNotFound("Invalid invitation code")
        if guest.account_type != "GUEST":
            raise ValidationError("User already converted")
        now = datetime.utcnow().isoformat()
        from domain.entities.user import User
        updated = User(
            user_id=guest.id,
            name=guest.name or user_data.get("name", ""),
            surname=guest.surname or user_data.get("surname", ""),
            username=guest.username or user_data.get("username", ""),
            email=guest.email or user_data.get("email", ""),
            avatar=guest.avatar or user_data.get("avatar"),
            account_type="USER",
            status="ACTIVE",
            level=guest.level or user_data.get("level"),
            position=guest.position or user_data.get("position"),
            dominant_hand=guest.dominant_hand or user_data.get("dominant_hand"),
            points=guest.points or 0,
            invited_by=guest.invited_by,
            invitation_code=guest.invitation_code,
            converted_at=now,
        )
        self.user_repo.save(updated)
        if guest.email:
            hashed = self.auth_service.hash_password(password or "password")
            self.user_repo.create_auth(guest.id, guest.email, hashed)
        role = self.user_repo.find_role_by_user(guest.id) or "PLAYER"
        token = self.auth_service.create_access_token(guest.id, role)
        return {"status": "converted", "user_id": guest.id, "access_token": token, "token_type": "bearer", "role": role}


class UpdateUserPrivacyUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, user_id, privacy_data):
        self.user_repo.update_privacy(user_id, privacy_data)
        return {"status": "updated"}
