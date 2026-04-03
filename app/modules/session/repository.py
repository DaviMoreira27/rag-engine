import redis.asyncio as aioredis
from app.modules.session.interface import SessionRepository

class RedisSessionRepository(SessionRepository):
    def __init__(self, r: aioredis.Redis):
        self.r = r

    async def save(self, session_id: str, data: dict, ttl: int, set_key: str | None = None) -> None:
        # type: ignore is required because redis-py methods return Union[Awaitable[int], int]
        # since the same class supports both sync and async usage, Pyright cannot infer
        # which one is being used at static analysis time.
        # this is a known issue and has not been released yet (7.4.0)
        # https://github.com/redis/redis-py/issues/2399
        await self.r.hset(session_id, mapping=data)  # type: ignore[misc]
            await self.r.expire(session_id, ttl)  # type: ignore[misc]
            if set_key:
                await self.r.sadd(set_key, session_id)  # type: ignore[misc]

    async def get(self, session_id: str) -> dict | None:
        data = await self.r.hgetall(session_id)  # type: ignore[misc]
        return data if data else None

    async def remove(self, session_id: str) -> None:
        data = await self.r.hgetall(session_id)  # type: ignore[misc]
        if data:
            await self.r.srem(f"tenant_sessions:{data['tenant_id']}", session_id)  # type: ignore[misc]
        await self.r.delete(session_id)  # type: ignore[misc]

    async def get_set_members(self, key: str) -> set[str]:
        return await self.r.smembers(key)  # type: ignore[misc]
