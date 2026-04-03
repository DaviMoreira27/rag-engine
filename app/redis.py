import redis
from app.config import Config

config = Config()

redis_config = Config.get_redis_config()

redis_db = redis.Redis(
    host=redis_config.host,
    port=redis_config.port,
    username=redis_config.username,
    password=redis_config.password,
    health_check_interval=30,
    decode_responses=True,
    connection_pool=redis.ConnectionPool(
        host=redis_config.host,
        port=redis_config.port,
        username=redis_config.username,
        password=redis_config.password,
        max_connections=redis_config.max_connections,
        decode_responses=True,
    )
)
