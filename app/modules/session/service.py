import redis.asyncio as asyncredis
from fastapi import Depends
from app.config import Config
from app.modules.session.interface import SessionRepository
from app.modules.session.repository import RedisSessionRepository
from app.redis import get_redis
from app.modules.user.model import User
from uuid import uuid4

class SessionService:
    def __init__(self, session_repository: SessionRepository, ttl: int):
        self.repository = session_repository
        self.time_to_live = ttl

    async def create_session(self, user: User) -> str:
        session_id = str(uuid4())
        await self.repository.save(
            session_id=session_id,
            data={"user_id": str(user.user_id), "tenant_id": str(user.tenant_id)},
            ttl=self.time_to_live,
            set_key=f"tenant_sessions:{user.tenant_id}"
        )
        return session_id

    async def get_session(self, session_id: str) -> dict | None:
        return await self.repository.get(session_id)

    async def remove_session(self, session_id: str) -> None:
        await self.repository.remove(session_id)

    async def bulk_remove_by_tenant(self, tenant_id: str) -> None:
        session_ids = await self.repository.get_set_members(f"tenant_sessions:{tenant_id}")
        for session_id in session_ids:
            await self.repository.remove(session_id)

def get_session_service(
    r: asyncredis.Redis = Depends(get_redis),
) -> SessionService:
    ttl = Config.get_session_ttl()
    repository = RedisSessionRepository(r=r)
    return SessionService(session_repository=repository, ttl=ttl)
