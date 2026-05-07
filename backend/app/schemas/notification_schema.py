from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.common.enums.notification_type import NotificationType


class NotificationBase(BaseModel):
    """Campos comunes para Notification."""

    user_id: int = Field(..., gt=0, description="ID del usuario")
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    type: NotificationType = Field(..., description="Tipo de notificación")


class NotificationCreate(NotificationBase):
    """Schema para crear una notificación."""

    pass


class NotificationUpdate(BaseModel):
    """Schema para actualizar una Notification."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    """Schema de respuesta para Notification."""

    id: int
    is_read: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
