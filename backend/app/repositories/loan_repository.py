from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.loan import Loan, LoanStatus
from app.schemas.loan_schema import LoanCreate, LoanUpdate


class LoanRepository:
    """Repositorio para operaciones de base de datos de Loan."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Obtener todos los préstamos con paginación."""
        return self.db.query(Loan).offset(skip).limit(limit).all()
    
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        """Obtener un préstamo por ID."""
        return self.db.query(Loan).filter(Loan.id == loan_id).first()
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Obtener préstamos de un usuario con paginación."""
        return self.db.query(Loan).filter(Loan.user_id == user_id).offset(skip).limit(limit).all()
    
    def get_active_loans_by_user(self, user_id: int) -> List[Loan]:
        """Obtener préstamos activos de un usuario."""
        return self.db.query(Loan).filter(
            and_(Loan.user_id == user_id, Loan.status == LoanStatus.ACTIVE)
        ).all()
    
    def get_active_loans_by_book(self, book_id: int) -> List[Loan]:
        """Obtener préstamos activos de un libro."""
        return self.db.query(Loan).filter(
            and_(Loan.book_id == book_id, Loan.status == LoanStatus.ACTIVE)
        ).all()
    
    def create(self, loan_data: LoanCreate) -> Loan:
        """Crear un nuevo préstamo."""
        db_loan = Loan(**loan_data.model_dump())
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan
    
    def update(self, loan_id: int, loan_data: LoanUpdate) -> Optional[Loan]:
        """Actualizar un préstamo existente."""
        db_loan = self.get_by_id(loan_id)
        if not db_loan:
            return None
        
        update_data = loan_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_loan, field, value)
        
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan
    
    def delete(self, loan_id: int) -> bool:
        """Eliminar un préstamo por ID."""
        db_loan = self.get_by_id(loan_id)
        if not db_loan:
            return False
        
        self.db.delete(db_loan)
        self.db.commit()
        return True
