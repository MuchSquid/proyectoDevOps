from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService


router = APIRouter(prefix="/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    """Dependency para obtener BookService."""
    return BookService(db)


@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
def get_books(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    book_service: BookService = Depends(get_book_service)
):
    """Obtener todos los libros con paginación."""
    return book_service.get_all_books(skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
):
    """Obtener un libro por ID."""
    book = book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    """Crear un nuevo libro."""
    return book_service.create_book(book_data)


@router.put("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
):
    """Actualizar un libro existente."""
    book = book_service.update_book(book_id, book_data)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
):
    """Eliminar un libro por ID."""
    success = book_service.delete_book(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
