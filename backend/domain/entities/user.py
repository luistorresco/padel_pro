"""User entity."""


class User:
    def __init__(
        self,
        user_id: str,
        name: str,
        surname: str,
        username: str,
        email: str,
        avatar: str | None,
        account_type: str,
        status: str,
        level: str | None,
        position: str | None,
        dominant_hand: str | None,
        points: int,
        invited_by: str | None = None,
        invitation_code: str | None = None,
        converted_at: str | None = None,
        deleted_at: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
    ):
        self.id = user_id
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.avatar = avatar
        self.account_type = account_type
        self.status = status
        self.level = level
        self.position = position
        self.dominant_hand = dominant_hand
        self.points = points
        self.invited_by = invited_by
        self.invitation_code = invitation_code
        self.converted_at = converted_at
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.updated_at = updated_at
