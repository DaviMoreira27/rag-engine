import pytest
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.database import Base
from app.core.redis import RedisDatabase
from app.core.config.service import Config
from app.modules.session.repository import RedisSessionRepository

@pytest.fixture
async def redis_client():
    client = aioredis.Redis(host="localhost", port=6379, db=RedisDatabase.TEST.value, decode_responses=True)
    yield client
    await client.flushdb()
    await client.aclose()


@pytest.fixture
async def repository(redis_client):
    return RedisSessionRepository(r=redis_client)


@pytest.fixture(scope="session")
def db_engine():
    return create_async_engine(Config.get_database_connection_url())


@pytest.fixture(scope="session", autouse=True)
async def setup_schema(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(db_engine):
    async with db_engine.connect() as conn:
        await conn.begin()
        session = AsyncSession(bind=conn, join_transaction_mode="create_savepoint")
        yield session
        await session.close()
        await conn.rollback()
