from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from app.main import app
from app.infrastructure.database.session import engine
from app.infrastructure.database.base import Base

# MOCK_USER_CREDENTIALS
MOCK_USER_EMAIL = "test@example.com"
MOCK_USER_PASSWORD = "Password123"


async def setup_mock_user(client: AsyncClient, email: str, password: str, is_admin: bool = False):
    """Utility function to register a user for testing purposes."""
    user_data = {
        "email": email,
        "password": password
    }
    response = await client.post("/v1/users/", json=user_data)
    assert response.status_code == 201
    return response.json()["data"]


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_database_cleanup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def auth_user_client(client: AsyncClient):
    """Fixture to create and authenticate a regular user."""
    user_read = await setup_mock_user(client, MOCK_USER_EMAIL, MOCK_USER_PASSWORD)
    login_data = {
        "username": MOCK_USER_EMAIL,
        "password": MOCK_USER_PASSWORD
    }
    response = await client.post("/v1/auth/token", data=login_data)
    tokens = response.json()["data"]
    client.headers["Authorization"] = f"Bearer {tokens['access_token']}"
    return client
