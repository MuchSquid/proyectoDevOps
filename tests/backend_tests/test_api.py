import pytest
from httpx import AsyncClient
from backend.app.main import app

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
    assert app.title == "Biblioteca Reservas API"

def test_example_math():
    assert 1 + 1 == 2
