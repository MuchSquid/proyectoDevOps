from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.fine import Fine
from app.schemas.fine_schema import FineCreate, FineUpdate


class FineRepository:
    """Repositorio para operaciones de base de datos de Fine."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Fine]:
        return self.db.query(Fine).offset(skip).limit(limit).all()

    def get_by_id(self, fine_id: int) -> Optional[Fine]:
        return self.db.query(Fine).filter(Fine.id == fine_id).first()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Fine]:
        return (
            self.db.query(Fine)
            .filter(Fine.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, fine_data: FineCreate) -> Fine:
        db_fine = Fine(**fine_data.model_dump())
        self.db.add(db_fine)
        self.db.commit()
        self.db.refresh(db_fine)
        return db_fine

    def update(self, fine_id: int, fine_data: FineUpdate) -> Optional[Fine]:
        db_fine = self.get_by_id(fine_id)
        if not db_fine:
            return None
        update_data = fine_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_fine, field, value)
        self.db.commit()
        self.db.refresh(db_fine)
        return db_fine
