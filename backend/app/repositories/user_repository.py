from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate


class UserRepository:
    """Repositorio para operaciones de base de datos de User."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtener todos los usuarios con paginación."""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener un usuario por ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener un usuario por email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_university_code(self, university_code: str) -> Optional[User]:
        """Obtener un usuario por código universitario."""
        return self.db.query(User).filter(User.university_code == university_code).first()
    
    def create(self, user_data: UserCreate) -> User:
        """Crear un nuevo usuario."""
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=user_data.password,  # El service hashear antes de llamar
            university_code=user_data.university_code,
            phone=user_data.phone,
            role=user_data.role,
            is_active=user_data.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Actualizar un usuario existente."""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "password":
                # El service hashear antes de llamar
                setattr(db_user, "password_hash", value)
            else:
                setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        """Eliminar un usuario por ID."""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
