import pytest
import redis.asyncio as aioredis
from app.modules.session.repository import RedisSessionRepository

@pytest.fixture
async def redis_client():
    client = aioredis.Redis(host="localhost", port=6379, db=15, decode_responses=True)
    yield client
    await client.flushdb()
    await client.aclose()

@pytest.fixture
async def repository(redis_client):
    return RedisSessionRepository(r=redis_client)

async def test_save_and_get(repository):
    await repository.save(
        session_id="session:abc123",
        data={"user_id": "user1", "tenant_id": "tenant1"},
        ttl=3600,
        set_key="tenant_sessions:tenant1"
    )
    data = await repository.get("session:abc123")
    assert data["user_id"] == "user1"
    assert data["tenant_id"] == "tenant1"

async def test_remove_cleans_set(repository):
    await repository.save(
        session_id="session:abc123",
        data={"user_id": "user1", "tenant_id": "tenant1"},
        ttl=3600,
        set_key="tenant_sessions:tenant1"
    )
    await repository.remove("session:abc123")
    data = await repository.get("session:abc123")
    members = await repository.get_set_members("tenant_sessions:tenant1")
    assert data is None
    assert "session:abc123" not in members

async def test_get_set_members(repository):
    await repository.save("session:abc123", {"user_id": "u1", "tenant_id": "t1"}, 3600, "tenant_sessions:t1")
    await repository.save("session:def456", {"user_id": "u2", "tenant_id": "t1"}, 3600, "tenant_sessions:t1")
    members = await repository.get_set_members("tenant_sessions:t1")
    assert "session:abc123" in members
    assert "session:def456" in members

async def test_ttl_is_set(repository, redis_client):
    await repository.save(
        session_id="session:abc123",
        data={"user_id": "user1", "tenant_id": "tenant1"},
        ttl=3600,
        set_key="tenant_sessions:tenant1"
    )
    ttl = await redis_client.ttl("session:abc123")
    assert ttl > 0
    assert ttl <= 3600
