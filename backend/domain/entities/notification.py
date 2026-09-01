"""Notification entity."""


class Notification:
    def __init__(
        self,
        notification_id: str,
        user_id: str,
        title: str,
        body: str | None = None,
        timestamp: str | None = None,
        read_status: bool = False,
        notification_type: str | None = None,
        link_id: str | None = None,
        created_at: str | None = None,
    ):
        self.id = notification_id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.timestamp = timestamp
        self.read_status = read_status
        self.type = notification_type
        self.link_id = link_id
        self.created_at = created_at
