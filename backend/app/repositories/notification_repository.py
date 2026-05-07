from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification_schema import NotificationCreate, NotificationUpdate


class NotificationRepository:
    """Repositorio para operaciones de base de datos de Notification."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Notification]:
        return self.db.query(Notification).offset(skip).limit(limit).all()

    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        return (
            self.db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def get_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_unread_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            self.db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, data: NotificationCreate) -> Notification:
        payload = data.model_dump()
        db_notification = Notification(**payload)
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification

    def update(
        self, notification_id: int, data: NotificationUpdate
    ) -> Optional[Notification]:
        db_notification = self.get_by_id(notification_id)
        if not db_notification:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_notification, field, value)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification
