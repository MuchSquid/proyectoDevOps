from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book_schema import BookCreate, BookUpdate


class BookRepository:
    """Repositorio para operaciones de base de datos de Book."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Obtener todos los libros con paginación."""
        return self.db.query(Book).offset(skip).limit(limit).all()
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Obtener un libro por ID."""
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def create(self, book_data: BookCreate) -> Book:
        """Crear un nuevo libro."""
        db_book = Book(**book_data.model_dump())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def update(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        """Actualizar un libro existente."""
        db_book = self.get_by_id(book_id)
        if not db_book:
            return None
        
        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def delete(self, book_id: int) -> bool:
        """Eliminar un libro por ID."""
        db_book = self.get_by_id(book_id)
        if not db_book:
            return False
        
        self.db.delete(db_book)
        self.db.commit()
        return True
