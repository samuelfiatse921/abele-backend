import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from app.deps.db.db import get_db_session
from app.main import app
from app.user.models.base import Base

# --- Setup test database ---
TEST_DATABASE_URL = "postgresql+asyncpg://user:pass@postgres/abele_test"

engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
AsyncTestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Fixture: create test database schema
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Fixture: provide async db session for routes
@pytest.fixture
async def db_session():
    async with AsyncTestingSessionLocal() as session:
        yield session


# Override get_db in FastAPI
@pytest.fixture(autouse=True)
def override_get_db(db_session):
    async def _get_test_db():
        async with AsyncTestingSessionLocal() as session:
            yield session
    app.dependency_overrides[get_db_session] = _get_test_db
    yield
    app.dependency_overrides.clear()


# Fixture: async client
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as c:
        yield c


# Example CRUD test
@pytest.mark.asyncio
async def test_create_and_get_user(client: AsyncClient):
    # create user
    response = await client.post("/api/v1/user", json={"username": "alice", "password": "secret"})
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["username"] == "alice"

    # get user
    response = await client.get(f"/users/{user_data['id']}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["username"] == "alice"
