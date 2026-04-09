from abc import abstractmethod, ABC
from .model import Tenant

class TenantRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, tenant_id: str) -> Tenant | None: ...
