from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.loan import Loan
    from app.models.reservation import Reservation


class Book(Base):
    """Modelo SQLAlchemy para la entidad Book."""
    
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    publication_year = Column(Integer, nullable=True)
    language = Column(String(50), nullable=True)
    pages = Column(Integer, nullable=True)
    publisher = Column(String(255), nullable=True)
    cover_image = Column(String(500), nullable=True)
    category_id = Column(Integer, nullable=True)
    available_copies = Column(Integer, nullable=False, default=1, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación bidireccional con Loan
    loans = relationship("Loan", back_populates="book")
    # Relación bidireccional con Reservation
    reservations = relationship("Reservation", back_populates="book")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"
