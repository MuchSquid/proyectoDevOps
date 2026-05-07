from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.loan import LoanStatus


class LoanBase(BaseModel):
    """Campos comunes para Loan."""
    user_id: int = Field(..., gt=0, description="ID del usuario")
    book_id: int = Field(..., gt=0, description="ID del libro")


class LoanCreate(LoanBase):
    """Schema para crear un Loan."""
    pass


class LoanUpdate(BaseModel):
    """Schema para actualizar un Loan (todos los campos opcionales)."""
    status: Optional[LoanStatus] = None
    returned_at: Optional[datetime] = None


class LoanResponse(LoanBase):
    """Schema para respuesta completa de Loan."""
    id: int
    loan_date: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None
    status: LoanStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
