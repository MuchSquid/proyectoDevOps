from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import book_router, user_router
from app.core.database import engine, Base


# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(book_router.router)
app.include_router(user_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Biblioteca Reservas API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
