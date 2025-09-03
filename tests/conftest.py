import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_session
from app.main import app

DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(  # type: ignore
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# @pytest_asyncio.fixture
# async def http_client():
#     """
#     Provides an async HTTP client for testing FastAPI endpoints.
#     Usage in tests:
#         async def test_example(http_client):
#             response = await http_client.get("/v1/users")
#     """
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://testserver") as client:
#         yield client

@pytest_asyncio.fixture
async def http_client(db_session: AsyncSession):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="session")
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_test_db):
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()
