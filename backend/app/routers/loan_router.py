from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse
from app.services.loan_service import LoanService


router = APIRouter(prefix="/loans", tags=["loans"])


def get_loan_service(db: Session = Depends(get_db)) -> LoanService:
    """Dependency para obtener LoanService."""
    return LoanService(db)


@router.get("/", response_model=List[LoanResponse], status_code=status.HTTP_200_OK)
def get_loans(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    loan_service: LoanService = Depends(get_loan_service)
):
    """Obtener todos los préstamos con paginación."""
    return loan_service.get_all_loans(skip=skip, limit=limit)


@router.get("/{loan_id}", response_model=LoanResponse, status_code=status.HTTP_200_OK)
def get_loan(
    loan_id: int,
    loan_service: LoanService = Depends(get_loan_service)
):
    """Obtener un préstamo por ID."""
    loan = loan_service.get_loan_by_id(loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with id {loan_id} not found"
        )
    return loan


@router.get("/user/{user_id}", response_model=List[LoanResponse], status_code=status.HTTP_200_OK)
def get_loans_by_user(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    loan_service: LoanService = Depends(get_loan_service)
):
    """Obtener préstamos de un usuario."""
    return loan_service.get_loans_by_user(user_id, skip=skip, limit=limit)


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan_data: LoanCreate,
    loan_service: LoanService = Depends(get_loan_service)
):
    """Crear un nuevo préstamo."""
    try:
        return loan_service.create_loan(loan_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{loan_id}/return", response_model=LoanResponse, status_code=status.HTTP_200_OK)
def return_loan(
    loan_id: int,
    loan_service: LoanService = Depends(get_loan_service)
):
    """Registrar devolución de un préstamo."""
    try:
        loan = loan_service.return_loan(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with id {loan_id} not found"
            )
        return loan
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{loan_id}/cancel", response_model=LoanResponse, status_code=status.HTTP_200_OK)
def cancel_loan(
    loan_id: int,
    loan_service: LoanService = Depends(get_loan_service)
):
    """Cancelar un préstamo."""
    try:
        loan = loan_service.cancel_loan(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with id {loan_id} not found"
            )
        return loan
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{loan_id}", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
def delete_loan(
    loan_id: int,
    loan_service: LoanService = Depends(get_loan_service)
):
    """Eliminar un préstamo (NO soportado - usar cancel)."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Physical deletion of loans is not supported. Use PATCH /loans/{loan_id}/cancel instead."
    )
