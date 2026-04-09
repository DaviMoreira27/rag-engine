from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.tenant.interface import TenantRepositoryPort
from app.modules.tenant.repository import TenantRepository
from app.modules.tenant.service import TenantService

def get_tenant_repository(db: AsyncSession = Depends(get_db)) -> TenantRepositoryPort:
    return TenantRepository(database=db)

def get_tenant_service(
    repo: TenantRepositoryPort = Depends(get_tenant_repository),
) -> TenantService:
    return TenantService(repository=repo)
