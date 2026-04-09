from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.modules.tenant.interface import TenantRepositoryPort

from .model import Tenant

class TenantRepository(TenantRepositoryPort):
    def __init__(self, database: AsyncSession):
        self.db = database

    async def get_by_id(self, tenant_id: str) -> Tenant | None:
        result = await self.db.execute(
            select(Tenant)
            .where(Tenant.tenant_id == tenant_id)
        )

        return result.scalar_one_or_none()
