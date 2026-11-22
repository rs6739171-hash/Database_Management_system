import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel

from main import app
from app.database.session import get_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_async_session = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(autouse=True)
async def init_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def override_get_session():
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient):
    # Register seller
    await client.post(
        "/seller/signup",
        json={
            "name": "Auth Seller",
            "email": "authseller@example.com",
            "password": "password123",
        },
    )
    # Login to obtain JWT
    login_res = await client.post(
        "/seller/login",
        data={"username": "authseller@example.com", "password": "password123"},
    )
    token = login_res.json()["access_token"]
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
    ) as auth_ac:
        yield auth_ac
