from app.modules.tenant.exception import TenantNotFoundError
from app.modules.tenant.interface import TenantRepositoryPort

class TenantService:
    def __init__(self, repository: TenantRepositoryPort):
        self.repo = repository

    async def ensure_exists(self, tenant_id: str) -> None:
        tenant = await self.repo.get_by_id(tenant_id)
        if not tenant:
            raise TenantNotFoundError("Tenant not found")
