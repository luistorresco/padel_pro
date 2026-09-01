"""Auth use cases."""

from domain.exceptions import EntityNotFound, ValidationError


class LoginUseCase:
    def __init__(self, user_repo, role_repo, auth_service):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.auth_service = auth_service

    def execute(self, email, password):
        auth_row = self.user_repo.find_auth_by_email(email)
        if not auth_row:
            raise EntityNotFound("Invalid credentials")
        if not self.auth_service.verify_password(password, auth_row["hashed_password"]):
            raise EntityNotFound("Invalid credentials")
        user_id = auth_row["user_id"]
        role = self.user_repo.find_role_by_user(user_id) or "PLAYER"
        self.user_repo.update_last_login(user_id)
        token = self.auth_service.create_access_token(user_id, role)
        return {"access_token": token, "token_type": "bearer", "user_id": user_id, "role": role}


class RegisterUseCase:
    def __init__(self, user_repo, auth_service):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, name, surname, username, email, password, role="PLAYER"):
        if not email or not password:
            raise ValidationError("Email and password are required")
        existing = self.user_repo.find_auth_by_email(email)
        if existing:
            raise ValidationError("Email already registered")
        user_id = "usr_" + __import__('datetime').datetime.utcnow().strftime("%Y%m%d%H%M%S")
        hashed = self.auth_service.hash_password(password)
        from domain.entities.user import User
        user = User(
            user_id=user_id, name=name, surname=surname or "", username=username or email.split("@")[0],
            email=email, avatar=None, account_type="USER", status="ACTIVE",
            level=None, position=None, dominant_hand=None, points=0
        )
        self.user_repo.save(user)
        self.user_repo.create_auth(user_id, email, hashed)
        self.user_repo.assign_role(user_id, role)
        token = self.auth_service.create_access_token(user_id, role)
        return {"access_token": token, "token_type": "bearer", "user_id": user_id, "role": role}


class GetCurrentUserUseCase:
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
        stats = user.get("stats") or {}
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
            "stats": stats,
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
        return self.privacy_service.apply_user_privacy(resp, pv, viewer_is_self=True)
