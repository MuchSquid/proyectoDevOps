from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.reservation import ReservationStatus


class ReservationBase(BaseModel):
    """Campos comunes para Reservation."""
    user_id: int = Field(..., gt=0, description="ID del usuario")
    book_id: int = Field(..., gt=0, description="ID del libro")


class ReservationCreate(ReservationBase):
    """Schema para crear un Reservation."""
    expiration_date: Optional[datetime] = Field(None, description="Fecha de vencimiento (por defecto 3 días)")


class ReservationUpdate(BaseModel):
    """Schema para actualizar un Reservation (todos los campos opcionales)."""
    status: Optional[ReservationStatus] = None


class ReservationResponse(ReservationBase):
    """Schema para respuesta completa de Reservation."""
    id: int
    reservation_date: datetime
    expiration_date: datetime
    status: ReservationStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
