import redis.asyncio as aioredis
from functools import lru_cache
from app.config import Config

@lru_cache # guarantees that the object is created a single time and reutilized on every injection
def get_redis() -> aioredis.Redis:
    redis_config = Config.get_redis_config()
    pool = aioredis.ConnectionPool(
        host=redis_config.host,
        port=redis_config.port,
        username=redis_config.username,
        password=redis_config.password,
        max_connections=redis_config.max_connections,
        decode_responses=True,
    )
    return aioredis.Redis(connection_pool=pool, health_check_interval=30, decode_responses=True)
