from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.notification_schema import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)


class NotificationService:
    """Servicio para lógica de negocio de Notification."""

    def __init__(self, db: Session):
        self.repository = NotificationRepository(db)
        self.user_repository = UserRepository(db)

    def get_all_notifications(
        self, skip: int = 0, limit: int = 100
    ) -> List[NotificationResponse]:
        items = self.repository.get_all(skip=skip, limit=limit)
        return [NotificationResponse.model_validate(n) for n in items]

    def get_notification_by_id(
        self, notification_id: int
    ) -> Optional[NotificationResponse]:
        n = self.repository.get_by_id(notification_id)
        if not n:
            return None
        return NotificationResponse.model_validate(n)

    def get_notifications_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[NotificationResponse]:
        items = self.repository.get_by_user_id(
            user_id, skip=skip, limit=limit
        )
        return [NotificationResponse.model_validate(n) for n in items]

    def get_unread_notifications_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[NotificationResponse]:
        items = self.repository.get_unread_by_user(
            user_id, skip=skip, limit=limit
        )
        return [NotificationResponse.model_validate(n) for n in items]

    def create_notification(self, data: NotificationCreate) -> NotificationResponse:
        user = self.user_repository.get_by_id(data.user_id)
        if not user:
            raise ValueError(f"User with id {data.user_id} not found")

        n = self.repository.create(data)
        return NotificationResponse.model_validate(n)

    def mark_as_read(self, notification_id: int) -> Optional[NotificationResponse]:
        n = self.repository.get_by_id(notification_id)
        if not n:
            raise ValueError(f"Notification with id {notification_id} not found")

        if n.is_read:
            return NotificationResponse.model_validate(n)

        updated = self.repository.update(
            notification_id, NotificationUpdate(is_read=True)
        )
        if not updated:
            return None
        return NotificationResponse.model_validate(updated)
