import pytest
import redis.asyncio as aioredis
from app.core.redis import RedisDatabase
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
