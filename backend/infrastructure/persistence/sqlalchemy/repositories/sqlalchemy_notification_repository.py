"""SQLAlchemy notification repository implementation."""

from typing import Optional, List
from sqlalchemy import text
from domain.entities.notification import Notification
from domain.repositories.notification_repository import INotificationRepository


class SQLAlchemyNotificationRepository(INotificationRepository):
    def __init__(self, engine):
        self.engine = engine

    def find_by_user(self, user_id: str) -> List[Notification]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT * FROM notifications WHERE user_id = :uid ORDER BY timestamp DESC
            """), {"uid": user_id}).mappings().all()
            return [self._to_entity(dict(row)) for row in rows]

    def save(self, notification: Notification) -> Notification:
        with self.engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO notifications (id, user_id, title, body, timestamp, read_status, type, link_id)
                VALUES (:id, :user_id, :title, :body, :timestamp, :read_status, :type, :link_id)
                ON DUPLICATE KEY UPDATE
                    title = VALUES(title), body = VALUES(body), read_status = VALUES(read_status),
                    type = VALUES(type), link_id = VALUES(link_id)
            """), {
                "id": notification.id, "user_id": notification.user_id,
                "title": notification.title, "body": notification.body,
                "timestamp": notification.timestamp,
                "read_status": 1 if notification.read_status else 0,
                "type": notification.type, "link_id": notification.link_id,
            })
        return notification

    def mark_as_read(self, notification_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                UPDATE notifications SET read_status = 1 WHERE id = :id
            """), {"id": notification_id})

    def _to_entity(self, row: dict) -> Notification:
        return Notification(
            notification_id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            body=row.get("body"),
            timestamp=row.get("timestamp"),
            read_status=bool(row.get("read_status", 0)),
            notification_type=row.get("type"),
            link_id=row.get("link_id"),
        )
