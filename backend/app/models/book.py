from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"
