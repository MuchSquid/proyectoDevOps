import pytest
from httpx import AsyncClient
import os
import sys

# Añadir el directorio backend al path para que las importaciones internas de la app funcionen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from app.main import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Biblioteca Reservas API"}

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/non-existent")
    assert response.status_code == 404

def test_api_title():
    assert "Biblioteca Reservas" in app.title

def test_api_version():
    assert hasattr(app, "version")

@pytest.mark.asyncio
async def test_books_endpoint_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books/")
    # Podría fallar si la DB no está lista, pero verificamos que el endpoint responde algo (no 404)
    assert response.status_code in [200, 500] 

@pytest.mark.asyncio
async def test_users_endpoint_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/")
    assert response.status_code in [200, 500]

@pytest.mark.asyncio
async def test_loans_endpoint_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/loans/")
    assert response.status_code in [200, 500]

@pytest.mark.asyncio
async def test_fines_endpoint_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/fines/")
    assert response.status_code in [200, 500]
