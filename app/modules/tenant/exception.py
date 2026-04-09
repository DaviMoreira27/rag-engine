from app.core.exceptions import NotFoundError


class TenantNotFoundError(NotFoundError):
    def __init__(self, message: str = "Tenant not found"):
        super().__init__(message, "TENANT_NOT_FOUND")
