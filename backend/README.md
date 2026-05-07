# Backend - Biblioteca Reservas API

Backend del sistema de gestión de biblioteca universitaria implementado con FastAPI y SQLAlchemy.

## Estructura del Proyecto

```
backend/
├── app/
│   ├── main.py                    # Aplicación FastAPI principal
│   ├── core/
│   │   ├── config.py              # Configuraciones de la aplicación
│   │   └── database.py            # Configuración de base de datos
│   ├── models/
│   │   └── book.py                # Modelo SQLAlchemy de Book
│   ├── schemas/
│   │   └── book_schema.py         # Schemas Pydantic para validación
│   ├── services/
│   │   └── book_service.py        # Lógica de negocio
│   ├── routers/
│   │   └── book_router.py         # Endpoints REST API
│   ├── repositories/
│   │   └── book_repository.py     # Acceso a datos
│   └── utils/                     # Utilidades (para futuro)
├── requirements.txt               # Dependencias Python
├── .env                           # Variables de entorno
├── Dockerfile                     # Configuración Docker
└── README.md                      # Este archivo
```

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **PostgreSQL**: Base de datos relacional
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

## Instalación Local

### Prerrequisitos

- Python 3.11+
- PostgreSQL 16.3+

### Pasos

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tu configuración
```

4. Ejecutar migraciones (tablas se crean automáticamente al iniciar):
```bash
uvicorn app.main:app --reload
```

## Ejecución con Docker

### Construir imagen
```bash
docker build -t biblioteca-backend .
```

### Ejecutar contenedor
```bash
docker run -p 8000:8000 --env-file .env biblioteca-backend
```

### Con Docker Compose
```bash
docker-compose up backend
```

## Endpoints API

### Books

- `GET /books/` - Listar todos los libros (paginación: skip, limit)
- `GET /books/{id}` - Obtener libro por ID
- `POST /books/` - Crear nuevo libro
- `PUT /books/{id}` - Actualizar libro existente
- `DELETE /books/{id}` - Eliminar libro

### Health Check

- `GET /` - Mensaje de bienvenida
- `GET /health` - Verificar estado del servicio

## Modelo Book

Campos:
- `id`: Identificador único (autoincrement)
- `title`: Título del libro (requerido)
- `description`: Descripción del libro (opcional)
- `publication_year`: Año de publicación (opcional)
- `language`: Idioma del libro (opcional)
- `pages`: Número de páginas (opcional)
- `publisher`: Editorial (opcional)
- `cover_image`: URL de imagen de portada (opcional)
- `category_id`: ID de categoría (opcional)
- `created_at`: Fecha de creación (automático)
- `updated_at`: Fecha de actualización (automático)

## Documentación

La documentación automática de la API está disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Ejecutar pruebas:
```bash
pytest
```

## Configuración

Variables de entorno en `.env`:
```
DATABASE_URL=postgresql://user:password@db:5432/biblioteca
APP_NAME=Biblioteca Reservas API
APP_VERSION=1.0.0
DEBUG=True
```

## Arquitectura

El backend sigue una arquitectura en capas:

1. **Models**: Definición de entidades de base de datos
2. **Schemas**: Validación de datos con Pydantic
3. **Repositories**: Acceso directo a datos (CRUD)
4. **Services**: Lógica de negocio
5. **Routers**: Endpoints HTTP y validación
6. **Core**: Configuraciones y utilidades compartidas
