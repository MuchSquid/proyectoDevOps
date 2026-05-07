from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.reservation_schema import ReservationCreate, ReservationUpdate


class ReservationRepository:
    """Repositorio para operaciones de base de datos de Reservation."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Reservation]:
        """Obtener todas las reservas con paginación."""
        return self.db.query(Reservation).offset(skip).limit(limit).all()
    
    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """Obtener una reserva por ID."""
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Reservation]:
        """Obtener reservas de un usuario con paginación."""
        return self.db.query(Reservation).filter(Reservation.user_id == user_id).offset(skip).limit(limit).all()
    
    def get_active_by_user_and_book(self, user_id: int, book_id: int) -> Optional[Reservation]:
        """Obtener reserva activa de un usuario para un libro específico."""
        return self.db.query(Reservation).filter(
            and_(
                Reservation.user_id == user_id,
                Reservation.book_id == book_id,
                Reservation.status == ReservationStatus.ACTIVE
            )
        ).first()
    
    def create(self, reservation_data: ReservationCreate) -> Reservation:
        """Crear una nueva reserva."""
        db_reservation = Reservation(**reservation_data.model_dump())
        self.db.add(db_reservation)
        self.db.commit()
        self.db.refresh(db_reservation)
        return db_reservation
    
    def update(self, reservation_id: int, reservation_data: ReservationUpdate) -> Optional[Reservation]:
        """Actualizar una reserva existente."""
        db_reservation = self.get_by_id(reservation_id)
        if not db_reservation:
            return None
        
        update_data = reservation_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reservation, field, value)
        
        self.db.commit()
        self.db.refresh(db_reservation)
        return db_reservation
    
    def delete(self, reservation_id: int) -> bool:
        """Eliminar una reserva por ID."""
        db_reservation = self.get_by_id(reservation_id)
        if not db_reservation:
            return False
        
        self.db.delete(db_reservation)
        self.db.commit()
        return True
