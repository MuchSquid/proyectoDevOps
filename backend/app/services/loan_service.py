from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.schemas.loan_schema import LoanCreate, LoanUpdate, LoanResponse
from app.schemas.book_schema import BookUpdate
from app.models.loan import LoanStatus


class LoanService:
    """Servicio para lógica de negocio de Loan."""
    
    def __init__(self, db: Session):
        self.repository = LoanRepository(db)
        self.book_repository = BookRepository(db)
        self.user_repository = UserRepository(db)
    
    def get_all_loans(self, skip: int = 0, limit: int = 100) -> List[LoanResponse]:
        """Obtener todos los préstamos."""
        loans = self.repository.get_all(skip=skip, limit=limit)
        return [LoanResponse.model_validate(loan) for loan in loans]
    
    def get_loan_by_id(self, loan_id: int) -> Optional[LoanResponse]:
        """Obtener un préstamo por ID."""
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            return None
        return LoanResponse.model_validate(loan)
    
    def get_loans_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[LoanResponse]:
        """Obtener préstamos de un usuario."""
        loans = self.repository.get_by_user_id(user_id, skip=skip, limit=limit)
        return [LoanResponse.model_validate(loan) for loan in loans]
    
    def create_loan(self, loan_data: LoanCreate) -> LoanResponse:
        """Crear un nuevo préstamo con validaciones de negocio."""
        # Validar que el usuario existe
        user = self.user_repository.get_by_id(loan_data.user_id)
        if not user:
            raise ValueError(f"User with id {loan_data.user_id} not found")
        
        # Validar que el usuario está activo
        if not user.is_active:
            raise ValueError(f"User with id {loan_data.user_id} is not active")
        
        # Validar que el libro existe
        book = self.book_repository.get_by_id(loan_data.book_id)
        if not book:
            raise ValueError(f"Book with id {loan_data.book_id} not found")
        
        # Validar stock disponible
        if book.available_copies <= 0:
            raise ValueError(f"Book with id {loan_data.book_id} has no available copies")
        
        # Validar máximo 3 préstamos activos por usuario
        active_loans = self.repository.get_active_loans_by_user(loan_data.user_id)
        if len(active_loans) >= 3:
            raise ValueError(f"User with id {loan_data.user_id} has reached maximum of 3 active loans")
        
        # Crear préstamo
        loan = self.repository.create(loan_data)
        
        # Disminuir stock del libro
        book.available_copies -= 1
        self.book_repository.update(loan_data.book_id, BookUpdate(available_copies=book.available_copies))
        
        return LoanResponse.model_validate(loan)
    
    def return_loan(self, loan_id: int) -> Optional[LoanResponse]:
        """Registrar devolución de un préstamo."""
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            raise ValueError(f"Loan with id {loan_id} not found")
        
        # Validar que el préstamo no haya sido devuelto
        if loan.status == LoanStatus.RETURNED:
            raise ValueError(f"Loan with id {loan_id} has already been returned")
        
        # Validar que el préstamo no esté cancelado
        if loan.status == LoanStatus.CANCELLED:
            raise ValueError(f"Loan with id {loan_id} is cancelled")
        
        # Actualizar estado y fecha de devolución
        update_data = LoanUpdate(
            status=LoanStatus.RETURNED,
            returned_at=datetime.utcnow()
        )
        loan = self.repository.update(loan_id, update_data)
        
        # Aumentar stock del libro
        book = self.book_repository.get_by_id(loan.book_id)
        if book:
            book.available_copies += 1
            self.book_repository.update(loan.book_id, BookUpdate(available_copies=book.available_copies))
        
        return LoanResponse.model_validate(loan)
    
    def cancel_loan(self, loan_id: int) -> Optional[LoanResponse]:
        """Cancelar un préstamo."""
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            raise ValueError(f"Loan with id {loan_id} not found")
        
        # Validar que el préstamo no haya sido devuelto
        if loan.status == LoanStatus.RETURNED:
            raise ValueError(f"Loan with id {loan_id} has already been returned")
        
        # Validar que el préstamo no esté cancelado
        if loan.status == LoanStatus.CANCELLED:
            raise ValueError(f"Loan with id {loan_id} is already cancelled")
        
        # Actualizar estado
        update_data = LoanUpdate(status=LoanStatus.CANCELLED)
        loan = self.repository.update(loan_id, update_data)
        
        # Aumentar stock del libro
        book = self.book_repository.get_by_id(loan.book_id)
        if book:
            book.available_copies += 1
            self.book_repository.update(loan.book_id, BookUpdate(available_copies=book.available_copies))
        
        return LoanResponse.model_validate(loan)
    
    def delete_loan(self, loan_id: int) -> bool:
        """Eliminar un préstamo (NO soportado)."""
        # NO permitir eliminación física de préstamos
        raise ValueError("Physical deletion of loans is not supported. Use cancel status instead.")
