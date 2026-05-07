from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.schemas.reservation_schema import ReservationCreate, ReservationUpdate, ReservationResponse
from app.models.reservation import ReservationStatus


class ReservationService:
    """Servicio para lógica de negocio de Reservation."""
    
    def __init__(self, db: Session):
        self.repository = ReservationRepository(db)
        self.book_repository = BookRepository(db)
        self.user_repository = UserRepository(db)
    
    def get_all_reservations(self, skip: int = 0, limit: int = 100) -> List[ReservationResponse]:
        """Obtener todas las reservas."""
        reservations = self.repository.get_all(skip=skip, limit=limit)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]
    
    def get_reservation_by_id(self, reservation_id: int) -> Optional[ReservationResponse]:
        """Obtener una reserva por ID."""
        reservation = self.repository.get_by_id(reservation_id)
        if not reservation:
            return None
        return ReservationResponse.model_validate(reservation)
    
    def get_reservations_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ReservationResponse]:
        """Obtener reservas de un usuario."""
        reservations = self.repository.get_by_user_id(user_id, skip=skip, limit=limit)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]
    
    def create_reservation(self, reservation_data: ReservationCreate) -> ReservationResponse:
        """Crear una nueva reserva con validaciones de negocio."""
        # Validar que el usuario existe
        user = self.user_repository.get_by_id(reservation_data.user_id)
        if not user:
            raise ValueError(f"User with id {reservation_data.user_id} not found")
        
        # Validar que el usuario está activo
        if not user.is_active:
            raise ValueError(f"User with id {reservation_data.user_id} is not active")
        
        # Validar que el libro existe
        book = self.book_repository.get_by_id(reservation_data.book_id)
        if not book:
            raise ValueError(f"Book with id {reservation_data.book_id} not found")
        
        # Validar que no haya copias disponibles (solo reservar si no hay stock)
        if book.available_copies > 0:
            raise ValueError(f"Book with id {reservation_data.book_id} has available copies. Reservations only allowed when available_copies == 0")
        
        # Validar que el usuario no tenga ya una reserva activa del mismo libro
        existing_reservation = self.repository.get_active_by_user_and_book(
            reservation_data.user_id,
            reservation_data.book_id
        )
        if existing_reservation:
            raise ValueError(f"User with id {reservation_data.user_id} already has an active reservation for book with id {reservation_data.book_id}")
        
        # Crear reserva
        reservation = self.repository.create(reservation_data)
        
        return ReservationResponse.model_validate(reservation)
    
    def cancel_reservation(self, reservation_id: int) -> Optional[ReservationResponse]:
        """Cancelar una reserva."""
        reservation = self.repository.get_by_id(reservation_id)
        if not reservation:
            raise ValueError(f"Reservation with id {reservation_id} not found")
        
        # Validar que la reserva no esté ya cancelada
        if reservation.status == ReservationStatus.CANCELLED:
            raise ValueError(f"Reservation with id {reservation_id} is already cancelled")
        
        # Validar que la reserva no esté completada
        if reservation.status == ReservationStatus.COMPLETED:
            raise ValueError(f"Reservation with id {reservation_id} is already completed")
        
        # Actualizar estado
        update_data = ReservationUpdate(status=ReservationStatus.CANCELLED)
        reservation = self.repository.update(reservation_id, update_data)
        
        return ReservationResponse.model_validate(reservation)
    
    def complete_reservation(self, reservation_id: int) -> Optional[ReservationResponse]:
        """Completar una reserva (para futuro flujo de préstamo)."""
        reservation = self.repository.get_by_id(reservation_id)
        if not reservation:
            raise ValueError(f"Reservation with id {reservation_id} not found")
        
        # Validar que la reserva no esté ya completada
        if reservation.status == ReservationStatus.COMPLETED:
            raise ValueError(f"Reservation with id {reservation_id} is already completed")
        
        # Validar que la reserva no esté cancelada
        if reservation.status == ReservationStatus.CANCELLED:
            raise ValueError(f"Reservation with id {reservation_id} is cancelled")
        
        # Validar que la reserva no esté expirada
        if reservation.status == ReservationStatus.EXPIRED:
            raise ValueError(f"Reservation with id {reservation_id} is expired")
        
        # Actualizar estado
        update_data = ReservationUpdate(status=ReservationStatus.COMPLETED)
        reservation = self.repository.update(reservation_id, update_data)
        
        return ReservationResponse.model_validate(reservation)
    
    def delete_reservation(self, reservation_id: int) -> bool:
        """Eliminar una reserva (NO soportado)."""
        # NO permitir eliminación física de reservas
        raise ValueError("Physical deletion of reservations is not supported. Use cancel status instead.")
