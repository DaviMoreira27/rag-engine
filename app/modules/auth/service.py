from app.modules.auth.exception import InvalidCredentialsError
from app.modules.auth.schema import CreateUserRequest

from app.modules.user.service import UserService
from app.modules.session.service import SessionService
from app.modules.crypto.interface import CryptoServicePort
from app.modules.tenant.service import TenantService

class AuthService:
    def __init__(
        self,
        user_service: UserService,
        session_service: SessionService,
        crypto_service: CryptoServicePort,
        tenant_service: TenantService
    ) -> None:
        self._user_service = user_service
        self._session_service = session_service
        self._crypto_service = crypto_service
        self._tenant_service = tenant_service

    async def login(self, email: str, password: str) -> str:
        user = await self._user_service.get_user_by_email(email)
        if not user:
            raise InvalidCredentialsError("Invalid credentials")

        is_valid = self._crypto_service.verify(user.password_hash, password)
        if not is_valid:
            raise InvalidCredentialsError("Invalid credentials")

        session_id = await self._session_service.create_session(user.user_id, user.tenant_id)
        return session_id

    async def sign_up(self, request: CreateUserRequest) -> str:
        await self._tenant_service.ensure_exists(request.tenant.tenant_id)
        await self._user_service.ensure_email_not_taken(request.email)

        password_hash = self._crypto_service.hash(request.password)
        user = await self._user_service.create_user(
            email=request.email,
            password_hash=password_hash,
            tenant_id=request.tenant.tenant_id,
            name=request.name,
        )
        session_id = await self._session_service.create_session(user.user_id, user.tenant_id)
        return session_id

    async def logout(self, session_id: str) -> None:
        await self._session_service.remove_session(session_id)

    async def logout_tenant(self, tenant_id: str) -> None:
        await self._session_service.bulk_remove_by_tenant(tenant_id)
