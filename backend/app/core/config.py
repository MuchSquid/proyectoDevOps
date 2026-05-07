from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuraciones básicas de la aplicación."""
    
    DATABASE_URL: str = "postgresql://user:password@db:5432/biblioteca"
    
    # Configuraciones de la aplicación
    APP_NAME: str = "Biblioteca Reservas API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Configuraciones de CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
