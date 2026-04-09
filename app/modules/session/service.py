from app.modules.session.interface import SessionRepository
from uuid import uuid4

class SessionService:
    def __init__(self, session_repository: SessionRepository, ttl: int):
        self.repository = session_repository
        self.time_to_live = ttl

    async def create_session(self, user_id: str, tenant_id: str) -> str:
        session_id = str(uuid4())
        await self.repository.save(
            session_id=session_id,
            data={"user_id": str(user_id), "tenant_id": str(tenant_id)},
            ttl=self.time_to_live,
            set_key=f"tenant_sessions:{tenant_id}"
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
