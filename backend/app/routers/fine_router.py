from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.fine_schema import FineCreate, FineResponse
from app.services.fine_service import FineService

router = APIRouter(prefix="/fines", tags=["fines"])


def get_fine_service(db: Session = Depends(get_db)) -> FineService:
    return FineService(db)


@router.get("/", response_model=List[FineResponse], status_code=status.HTTP_200_OK)
def get_fines(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(
        10, gt=0, le=100, description="Número máximo de registros a retornar"
    ),
    fine_service: FineService = Depends(get_fine_service),
):
    return fine_service.get_all_fines(skip=skip, limit=limit)


@router.get(
    "/user/{user_id}",
    response_model=List[FineResponse],
    status_code=status.HTTP_200_OK,
)
def get_fines_by_user(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(
        10, gt=0, le=100, description="Número máximo de registros a retornar"
    ),
    fine_service: FineService = Depends(get_fine_service),
):
    return fine_service.get_fines_by_user(user_id, skip=skip, limit=limit)


@router.get("/{fine_id}", response_model=FineResponse, status_code=status.HTTP_200_OK)
def get_fine(
    fine_id: int,
    fine_service: FineService = Depends(get_fine_service),
):
    fine = fine_service.get_fine_by_id(fine_id)
    if not fine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fine with id {fine_id} not found",
        )
    return fine


@router.post("/", response_model=FineResponse, status_code=status.HTTP_201_CREATED)
def create_fine(
    fine_data: FineCreate,
    fine_service: FineService = Depends(get_fine_service),
):
    try:
        return fine_service.create_fine(fine_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch("/{fine_id}/pay", response_model=FineResponse, status_code=status.HTTP_200_OK)
def pay_fine(
    fine_id: int,
    fine_service: FineService = Depends(get_fine_service),
):
    try:
        fine = fine_service.pay_fine(fine_id)
        if not fine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fine with id {fine_id} not found",
            )
        return fine
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{fine_id}/cancel", response_model=FineResponse, status_code=status.HTTP_200_OK
)
def cancel_fine(
    fine_id: int,
    fine_service: FineService = Depends(get_fine_service),
):
    try:
        fine = fine_service.cancel_fine(fine_id)
        if not fine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fine with id {fine_id} not found",
            )
        return fine
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
