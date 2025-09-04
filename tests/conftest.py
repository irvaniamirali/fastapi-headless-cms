import uuid

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.domain.user.usecases.register_user import RegisterUser
from app.domain.user.models import User
from app.domain.user.schemas import UserCreate
from app.domain.user.repositories import UserRepository
from app.domain.post.repositories import PostRepository
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


@pytest_asyncio.fixture
async def http_client(db_session: AsyncSession):
    """
    Provides an async HTTP client for testing FastAPI endpoints.
    Usage in tests:
        async def test_example(http_client):
            response = await http_client.get("/v1/users")
    """

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


@pytest_asyncio.fixture
async def registered_user(db_session):
    """
    Fixture to create a registered user with a unique email for each test.
    """
    unique_email = f"test_post_user_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "StrongPassword123!"
    }
    user_repository = UserRepository(db_session, User)
    user_schema = UserCreate(**user_data)
    user = await RegisterUser(user_repository).execute(user_schema)
    return user


@pytest_asyncio.fixture
async def registered_user2(db_session):
    """
    Fixture to create a second registered user with a unique email for permission tests.
    """
    unique_email = f"test_post_user2_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "StrongPassword123!"
    }
    user_repository = UserRepository(db_session, User)
    user_schema = UserCreate(**user_data)
    user = await RegisterUser(user_repository).execute(user_schema)
    return user


@pytest_asyncio.fixture
async def create_post_fixture(db_session, registered_user):
    """
    Fixture to create a post for tests.
    """
    async def _create_post(title: str = "Test Post", content: str = "This is a test post content.", author=registered_user):
        post_repository = PostRepository(db_session)
        post = await post_repository.create(
            title=title,
            content=content,
            author_id=author.id
        )
        return post
    return _create_post
