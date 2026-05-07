from sqlalchemy import String, Integer, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.core.database import Base
from app.common.mixins.timestamp_mixin import TimestampMixin
from app.common.enums.notification_type import NotificationType

if TYPE_CHECKING:
    from app.models.user import User


class Notification(Base, TimestampMixin):
    """Notificación interna para un usuario."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[NotificationType] = mapped_column(
        "type", SQLEnum(NotificationType), nullable=False
    )
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type='{self.type}')>"
