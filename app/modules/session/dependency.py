import redis.asyncio as asyncredis

from fastapi import Depends

from app.core.config.service import Config
from app.modules.session.repository import RedisSessionRepository
from app.modules.session.service import SessionService
from app.core.redis import get_session_redis


def get_session_service(
    r: asyncredis.Redis = Depends(get_session_redis),
) -> SessionService:
    ttl = Config.get_session_ttl()
    repository = RedisSessionRepository(r=r)
    return SessionService(session_repository=repository, ttl=ttl)
