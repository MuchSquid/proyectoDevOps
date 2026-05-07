from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency para obtener UserService."""
    return UserService(db)


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    user_service: UserService = Depends(get_user_service)
):
    """Obtener todos los usuarios con paginación."""
    return user_service.get_all_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Obtener un usuario por ID."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Crear un nuevo usuario."""
    try:
        return user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Actualizar un usuario existente."""
    try:
        user = user_service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Eliminar un usuario por ID."""
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
