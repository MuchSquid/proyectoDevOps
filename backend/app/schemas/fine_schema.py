from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.common.enums.fine_status import FineStatus


class FineBase(BaseModel):
    """Campos comunes para Fine."""

    user_id: int = Field(..., gt=0, description="ID del usuario")
    loan_id: int = Field(..., gt=0, description="ID del préstamo")
    amount: Decimal = Field(..., gt=0, description="Monto de la multa")
    reason: str = Field(..., min_length=1, description="Motivo de la multa")


class FineCreate(FineBase):
    """Schema para crear una multa."""

    pass


class FineUpdate(BaseModel):
    """Schema para actualizar una Fine (campos opcionales)."""

    status: Optional[FineStatus] = None
    paid_at: Optional[datetime] = None
    reason: Optional[str] = None


class FineResponse(FineBase):
    """Schema de respuesta para Fine."""

    id: int
    status: FineStatus
    issued_at: datetime
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
