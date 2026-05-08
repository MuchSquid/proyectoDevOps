import os
import sys
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio actual al path para poder importar la app
sys.path.append(os.getcwd())

from app.core.config import settings
from app.models.book import Book
from app.models.user import User, UserRole
from app.models.loan import Loan
from app.models.reservation import Reservation
from app.models.fine import Fine
from app.models.notification import Notification
from app.core.database import Base, engine

# Configuración de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def seed():
    print("🌱 Iniciando siembra de datos...")
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Crear Usuario de prueba (si no existe)
        user_email = "admin@biblioteca.com"
        existing_user = db.query(User).filter(User.email == user_email).first()
        if not existing_user:
            print("👤 Creando usuario administrador...")
            new_user = User(
                first_name="Admin",
                last_name="Sistema",
                email=user_email,
                password_hash=hash_password("admin123"),
                university_code="ADMIN001",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(new_user)
        
        # 2. Crear un Estudiante de prueba
        student_email = "estudiante@u.edu"
        if not db.query(User).filter(User.email == student_email).first():
            print("👤 Creando estudiante de prueba...")
            new_student = User(
                first_name="Juan",
                last_name="Pérez",
                email=student_email,
                password_hash=hash_password("estudiante123"),
                university_code="2024001",
                role=UserRole.STUDENT,
                is_active=True
            )
            db.add(new_student)

        # 3. Insertar Libros
        books_to_add = [
            {
                "title": "Cien años de soledad",
                "description": "La obra maestra de Gabriel García Márquez.",
                "publication_year": 1967,
                "language": "Español",
                "pages": 417,
                "publisher": "Editorial Sudamericana",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9780307474728-L.jpg",
                "available_copies": 5
            },
            {
                "title": "El Principito",
                "description": "Una fábula poética y filosófica.",
                "publication_year": 1943,
                "language": "Español",
                "pages": 96,
                "publisher": "Reynal & Hitchcock",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9780156013925-L.jpg",
                "available_copies": 10
            },
            {
                "title": "1984",
                "description": "Novela distópica sobre la vigilancia absoluta.",
                "publication_year": 1949,
                "language": "Español",
                "pages": 328,
                "publisher": "Secker & Warburg",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg",
                "available_copies": 3
            },
            {
                "title": "Don Quijote de la Mancha",
                "description": "La historia del caballero andante.",
                "publication_year": 1605,
                "language": "Español",
                "pages": 1056,
                "publisher": "Francisco de Robles",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9788424116811-L.jpg",
                "available_copies": 2
            },
            {
                "title": "El Hobbit",
                "description": "La precuela de El Señor de los Anillos.",
                "publication_year": 1937,
                "language": "Español",
                "pages": 310,
                "publisher": "George Allen & Unwin",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9780345339683-L.jpg",
                "available_copies": 7
            },
            {
                "title": "El Alquimista",
                "description": "Un joven pastor viaja en busca de su tesoro personal.",
                "publication_year": 1988,
                "language": "Español",
                "pages": 208,
                "publisher": "HarperCollins",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg",
                "available_copies": 4
            },
            {
                "title": "Rayuela",
                "description": "Una de las obras centrales del boom latinoamericano.",
                "publication_year": 1963,
                "language": "Español",
                "pages": 600,
                "publisher": "Editorial Sudamericana",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9788420432366-L.jpg",
                "available_copies": 6
            },
            {
                "title": "Crónica de una muerte anunciada",
                "description": "Una novela corta que narra el asesinato de Santiago Nasar.",
                "publication_year": 1981,
                "language": "Español",
                "pages": 158,
                "publisher": "La Oveja Negra",
                "cover_image": "https://covers.openlibrary.org/b/isbn/9788420434445-L.jpg",
                "available_copies": 3
            }
        ]

        print("🧹 Limpiando tabla de libros...")
        db.query(Book).delete()
        
        print("📚 Insertando nuevos libros con portadas actualizadas...")
        for b_data in books_to_add:
            new_book = Book(**b_data)
            db.add(new_book)
        
        db.commit()
        print("✅ ¡Datos actualizados correctamente!")
        
    except Exception as e:
        print(f"❌ Error al sembrar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
