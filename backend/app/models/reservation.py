from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, text
from enum import Enum
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.book import Book
    from app.models.user import User


class ReservationStatus(str, Enum):
    """Enum para estados de reserva."""
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Reservation(Base):
    """Modelo SQLAlchemy para la entidad Reservation (estilo moderno SQLAlchemy 2.0)."""
    
    __tablename__ = "reservations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    reservation_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expiration_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("NOW() + INTERVAL '3 days'"))
    status: Mapped[ReservationStatus] = mapped_column(SQLEnum(ReservationStatus), nullable=False, default=ReservationStatus.ACTIVE)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones bidireccionales
    user: Mapped["User"] = relationship("User", back_populates="reservations")
    book: Mapped["Book"] = relationship("Book", back_populates="reservations")
    
    def __repr__(self):
        return f"<Reservation(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status='{self.status}')>"
