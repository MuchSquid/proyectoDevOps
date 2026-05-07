from typing import List, Optional
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
from app.repositories.fine_repository import FineRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.user_repository import UserRepository
from app.schemas.fine_schema import FineCreate, FineUpdate, FineResponse
from app.common.enums.fine_status import FineStatus


class FineService:
    """Servicio para lógica de negocio de Fine."""

    def __init__(self, db: Session):
        self.repository = FineRepository(db)
        self.loan_repository = LoanRepository(db)
        self.user_repository = UserRepository(db)

    def get_all_fines(self, skip: int = 0, limit: int = 100) -> List[FineResponse]:
        fines = self.repository.get_all(skip=skip, limit=limit)
        return [FineResponse.model_validate(f) for f in fines]

    def get_fine_by_id(self, fine_id: int) -> Optional[FineResponse]:
        fine = self.repository.get_by_id(fine_id)
        if not fine:
            return None
        return FineResponse.model_validate(fine)

    def get_fines_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[FineResponse]:
        fines = self.repository.get_by_user_id(user_id, skip=skip, limit=limit)
        return [FineResponse.model_validate(f) for f in fines]

    def create_fine(self, data: FineCreate) -> FineResponse:
        user = self.user_repository.get_by_id(data.user_id)
        if not user:
            raise ValueError(f"User with id {data.user_id} not found")
        if not user.is_active:
            raise ValueError(f"User with id {data.user_id} is not active")

        loan = self.loan_repository.get_by_id(data.loan_id)
        if not loan:
            raise ValueError(f"Loan with id {data.loan_id} not found")

        if loan.user_id != data.user_id:
            raise ValueError(
                "Fine user_id must match the loan's user_id"
            )

        if data.amount <= Decimal("0"):
            raise ValueError("amount must be greater than 0")

        fine = self.repository.create(data)
        return FineResponse.model_validate(fine)

    def pay_fine(self, fine_id: int) -> Optional[FineResponse]:
        fine = self.repository.get_by_id(fine_id)
        if not fine:
            raise ValueError(f"Fine with id {fine_id} not found")

        if fine.status == FineStatus.PAID:
            raise ValueError(f"Fine with id {fine_id} is already paid")

        if fine.status == FineStatus.CANCELLED:
            raise ValueError(
                f"Fine with id {fine_id} is cancelled and cannot be paid"
            )

        now = datetime.now(timezone.utc)
        updated = self.repository.update(
            fine_id,
            FineUpdate(status=FineStatus.PAID, paid_at=now),
        )
        if not updated:
            return None
        return FineResponse.model_validate(updated)

    def cancel_fine(self, fine_id: int) -> Optional[FineResponse]:
        fine = self.repository.get_by_id(fine_id)
        if not fine:
            raise ValueError(f"Fine with id {fine_id} not found")

        if fine.status == FineStatus.PAID:
            raise ValueError(
                f"Fine with id {fine_id} is paid and cannot be cancelled"
            )

        if fine.status == FineStatus.CANCELLED:
            raise ValueError(f"Fine with id {fine_id} is already cancelled")

        updated = self.repository.update(
            fine_id, FineUpdate(status=FineStatus.CANCELLED)
        )
        if not updated:
            return None
        return FineResponse.model_validate(updated)
