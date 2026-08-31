import json
from typing import List, Dict, Any

from sqlalchemy import text

from domain.repositories.notification_repository import NotificationRepository
from infrastructure.config.database import engine


class SqlNotificationRepository(NotificationRepository):
    def get_all(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM notifications ORDER BY timestamp DESC"))
            return [dict(row) for row in result.mappings()]

    def create(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO notifications (id, user_id, title, body, timestamp, read_status, type, link_id)
                VALUES (:id, :user_id, :title, :body, :timestamp, :read_status, :type, :link_id)
                ON DUPLICATE KEY UPDATE
                    title = VALUES(title), body = VALUES(body), read_status = VALUES(read_status),
                    type = VALUES(type), link_id = VALUES(link_id)
            """), {
                "id": notification_data["id"], "user_id": notification_data.get("user_id"),
                "title": notification_data["title"], "body": notification_data.get("body"),
                "timestamp": notification_data["timestamp"], "read_status": 1 if notification_data.get("read") else 0,
                "type": notification_data.get("type"), "link_id": notification_data.get("link_id"),
            })
        return notification_data
