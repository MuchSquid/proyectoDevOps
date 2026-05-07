from sqlalchemy import Integer, DateTime, Enum as SQLEnum, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from decimal import Decimal
from typing import TYPE_CHECKING
from app.core.database import Base
from app.common.mixins.timestamp_mixin import TimestampMixin
from app.common.enums.fine_status import FineStatus

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.loan import Loan


class Fine(Base, TimestampMixin):
    """Multa asociada a un préstamo y un usuario."""

    __tablename__ = "fines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    loan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[FineStatus] = mapped_column(
        SQLEnum(FineStatus), nullable=False, default=FineStatus.PENDING
    )
    issued_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    paid_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="fines")
    loan: Mapped["Loan"] = relationship("Loan", back_populates="fines")

    def __repr__(self):
        return f"<Fine(id={self.id}, user_id={self.user_id}, loan_id={self.loan_id}, status='{self.status}')>"
