import pytest
from httpx import AsyncClient
from main import app
from app.core.database import get_db

async def override_get_db():
    try:

        print("\n--- ПІДМІНА СПРАЦЮВАЛА: Використовується тестова БД ---")
        yield "mock_session" 
    finally:
        pass


app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_user_mock():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/me") 
        assert response.status_code == 401 