from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, text
from enum import Enum
from typing import TYPE_CHECKING
from app.core.database import Base
from app.common.mixins.timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from app.models.book import Book
    from app.models.user import User
    from app.models.fine import Fine


class LoanStatus(str, Enum):
    """Enum para estados de préstamo."""
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class Loan(Base, TimestampMixin):
    """Modelo SQLAlchemy para la entidad Loan (estilo moderno SQLAlchemy 2.0)."""
    
    __tablename__ = "loans"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    loan_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    due_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("NOW() + INTERVAL '14 days'"))
    returned_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[LoanStatus] = mapped_column(SQLEnum(LoanStatus), nullable=False, default=LoanStatus.ACTIVE)
    
    # Relaciones bidireccionales
    user: Mapped["User"] = relationship("User", back_populates="loans")
    book: Mapped["Book"] = relationship("Book", back_populates="loans")
    fines: Mapped[list["Fine"]] = relationship("Fine", back_populates="loan")
    
    def __repr__(self):
        return f"<Loan(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status='{self.status}')>"
