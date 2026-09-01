"""Notifications use cases."""

from domain.exceptions import EntityNotFound


class ListNotificationsUseCase:
    def __init__(self, notification_repo):
        self.notification_repo = notification_repo

    def execute(self, user_id):
        return self.notification_repo.find_by_user(user_id)


class CreateNotificationUseCase:
    def __init__(self, notification_repo):
        self.notification_repo = notification_repo

    def execute(self, notification_data):
        import uuid
        from domain.entities.notification import Notification
        notif_id = notification_data.get("id") or f"notif_{uuid.uuid4().hex[:8]}"
        n = Notification(
            notification_id=notif_id,
            user_id=notification_data.get("user_id"),
            title=notification_data["title"],
            body=notification_data.get("body"),
            timestamp=notification_data.get("timestamp"),
            read_status=bool(notification_data.get("read")),
            notification_type=notification_data.get("type"),
            link_id=notification_data.get("link_id"),
        )
        saved = self.notification_repo.save(n)
        return {"id": notif_id}
