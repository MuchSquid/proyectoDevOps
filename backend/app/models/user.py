from sqlalchemy import String, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from enum import Enum
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.loan import Loan
    from app.models.reservation import Reservation


class UserRole(str, Enum):
    """Enum para roles de usuario."""
    STUDENT = "STUDENT"
    LIBRARIAN = "LIBRARIAN"
    ADMIN = "ADMIN"


class User(Base):
    """Modelo SQLAlchemy para la entidad User (estilo moderno SQLAlchemy 2.0)."""
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    university_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación bidireccional con Loan
    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="user")
    # Relación bidireccional con Reservation
    reservations: Mapped[list["Reservation"]] = relationship("Reservation", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
