from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.book_repository import BookRepository
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse


class BookService:
    """Servicio para lógica de negocio de Book."""
    
    def __init__(self, db: Session):
        self.repository = BookRepository(db)
    
    def get_all_books(self, skip: int = 0, limit: int = 100) -> List[BookResponse]:
        """Obtener todos los libros."""
        books = self.repository.get_all(skip=skip, limit=limit)
        return [BookResponse.model_validate(book) for book in books]
    
    def get_book_by_id(self, book_id: int) -> Optional[BookResponse]:
        """Obtener un libro por ID."""
        book = self.repository.get_by_id(book_id)
        if not book:
            return None
        return BookResponse.model_validate(book)
    
    def create_book(self, book_data: BookCreate) -> BookResponse:
        """Crear un nuevo libro."""
        book = self.repository.create(book_data)
        return BookResponse.model_validate(book)
    
    def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[BookResponse]:
        """Actualizar un libro existente."""
        book = self.repository.update(book_id, book_data)
        if not book:
            return None
        return BookResponse.model_validate(book)
    
    def delete_book(self, book_id: int) -> bool:
        """Eliminar un libro por ID."""
        return self.repository.delete(book_id)
