from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.reservation_schema import ReservationCreate, ReservationResponse
from app.services.reservation_service import ReservationService


router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_reservation_service(db: Session = Depends(get_db)) -> ReservationService:
    """Dependency para obtener ReservationService."""
    return ReservationService(db)


@router.get("/", response_model=List[ReservationResponse], status_code=status.HTTP_200_OK)
def get_reservations(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """Obtener todas las reservas con paginación."""
    return reservation_service.get_all_reservations(skip=skip, limit=limit)


@router.get("/{reservation_id}", response_model=ReservationResponse, status_code=status.HTTP_200_OK)
def get_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """Obtener una reserva por ID."""
    reservation = reservation_service.get_reservation_by_id(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    return reservation


@router.get("/user/{user_id}", response_model=List[ReservationResponse], status_code=status.HTTP_200_OK)
def get_reservations_by_user(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """Obtener reservas de un usuario."""
    return reservation_service.get_reservations_by_user(user_id, skip=skip, limit=limit)


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_data: ReservationCreate,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """Crear una nueva reserva."""
    try:
        return reservation_service.create_reservation(reservation_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{reservation_id}/cancel", response_model=ReservationResponse, status_code=status.HTTP_200_OK)
def cancel_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """Cancelar una reserva."""
    try:
        reservation = reservation_service.cancel_reservation(reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reservation with id {reservation_id} not found"
            )
        return reservation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{reservation_id}/complete", response_model=ReservationResponse, status_code=status.HTTP_200_OK)
def complete_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """Completar una reserva."""
    try:
        reservation = reservation_service.complete_reservation(reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reservation with id {reservation_id} not found"
            )
        return reservation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{reservation_id}", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
def delete_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    """Eliminar una reserva (NO soportado - usar cancel)."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Physical deletion of reservations is not supported. Use PATCH /reservations/{reservation_id}/cancel instead."
    )
