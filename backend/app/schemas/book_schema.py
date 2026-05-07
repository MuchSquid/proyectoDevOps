from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    """Campos comunes para Book."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    publication_year: Optional[int] = Field(None, ge=1000, le=2100)
    language: Optional[str] = Field(None, max_length=50)
    pages: Optional[int] = Field(None, gt=0)
    publisher: Optional[str] = Field(None, max_length=255)
    cover_image: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None
    available_copies: int = Field(1, ge=0, description="Número de copias disponibles")


class BookCreate(BookBase):
    """Schema para crear un Book."""
    pass


class BookUpdate(BaseModel):
    """Schema para actualizar un Book (todos los campos opcionales)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    publication_year: Optional[int] = Field(None, ge=1000, le=2100)
    language: Optional[str] = Field(None, max_length=50)
    pages: Optional[int] = Field(None, gt=0)
    publisher: Optional[str] = Field(None, max_length=255)
    cover_image: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None


class BookResponse(BookBase):
    """Schema para respuesta completa de Book."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
