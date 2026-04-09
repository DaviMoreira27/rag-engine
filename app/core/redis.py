from enum import Enum
import redis.asyncio as aioredis
from functools import lru_cache
from app.core.config.service import Config

class RedisDatabase(Enum):
    SESSION = 0
    CACHE = 1
    TEST = 15

@lru_cache # guarantees that the object is created a single time and reutilized on every injection
def get_redis(db: int = RedisDatabase.SESSION.value) -> aioredis.Redis:
    redis_config = Config.get_redis_config()
    pool = aioredis.ConnectionPool(
        host=redis_config.host,
        port=redis_config.port,
        username=redis_config.username,
        password=redis_config.password,
        max_connections=redis_config.max_connections,
        decode_responses=True,
        db=db,
    )
    return aioredis.Redis(connection_pool=pool, health_check_interval=30, decode_responses=True)

def get_session_redis() -> aioredis.Redis:
    return get_redis(RedisDatabase.SESSION)

def get_cache_redis() -> aioredis.Redis:
    return get_redis(RedisDatabase.CACHE)

def get_test_redis() -> aioredis.Redis:
    return get_redis(RedisDatabase.TEST)
