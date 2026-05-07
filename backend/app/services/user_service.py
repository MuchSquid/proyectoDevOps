from typing import List, Optional
from sqlalchemy.orm import Session
import bcrypt
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.models.user import UserRole


class UserService:
    """Servicio para lógica de negocio de User."""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def hash_password(self, password: str) -> str:
        """Hashea un password usando bcrypt."""
        # Truncar a 72 bytes (límite de bcrypt)
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Obtener todos los usuarios."""
        users = self.repository.get_all(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Obtener un usuario por ID."""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Crear un nuevo usuario con password hasheado."""
        # Validar email único
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"Email {user_data.email} ya está registrado")
        
        # Validar university_code único
        existing_code = self.repository.get_by_university_code(user_data.university_code)
        if existing_code:
            raise ValueError(f"Código universitario {user_data.university_code} ya está registrado")
        
        # Hashear password
        password_hash = self.hash_password(user_data.password)
        
        # Crear usuario con password hasheado
        user_dict = user_data.model_dump()
        user_dict["password"] = password_hash  # El repository lo asigna a password_hash
        
        user = self.repository.create(UserCreate(**user_dict))
        return UserResponse.model_validate(user)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """Actualizar un usuario existente."""
        # Si se actualiza email, validar unicidad
        if user_data.email:
            existing_user = self.repository.get_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"Email {user_data.email} ya está registrado")
        
        # Si se actualiza university_code, validar unicidad
        if user_data.university_code:
            existing_code = self.repository.get_by_university_code(user_data.university_code)
            if existing_code and existing_code.id != user_id:
                raise ValueError(f"Código universitario {user_data.university_code} ya está registrado")
        
        # Si se actualiza password, hashear
        update_dict = user_data.model_dump(exclude_unset=True)
        if "password" in update_dict:
            update_dict["password"] = self.hash_password(update_dict["password"])
        
        user = self.repository.update(user_id, UserUpdate(**update_dict))
        if not user:
            return None
        return UserResponse.model_validate(user)
    
    def delete_user(self, user_id: int) -> bool:
        """Eliminar un usuario por ID."""
        return self.repository.delete(user_id)
