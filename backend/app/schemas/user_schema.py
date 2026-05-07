from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Campos comunes para User."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    university_code: str = Field(..., min_length=1, max_length=20)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.STUDENT
    is_active: bool = True


class UserCreate(UserBase):
    """Schema para crear un User (incluye password plaintext para hashing)."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema para actualizar un User (todos los campos opcionales excepto password_hash)."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    university_code: Optional[str] = Field(None, min_length=1, max_length=20)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """Schema para respuesta completa de User (NO incluye password_hash)."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
