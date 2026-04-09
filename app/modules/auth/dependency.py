from fastapi import Depends

from app.modules.auth.service import AuthService
from app.modules.session.service import SessionService

from app.modules.crypto.interface import CryptoServicePort

from app.modules.tenant.dependency import get_tenant_service
from app.modules.user.dependency import get_user_service
from app.modules.session.dependency import get_session_service
from app.modules.crypto.dependency import get_crypto_service

from app.modules.tenant.service import TenantService
from app.modules.user.service import UserService
from app.modules.auth.service import AuthService


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
    session_service: SessionService = Depends(get_session_service),
    crypto_service: CryptoServicePort = Depends(get_crypto_service),
    tenant_service: TenantService = Depends(get_tenant_service),
) -> AuthService:
    return AuthService(
        user_service=user_service,
        session_service=session_service,
        crypto_service=crypto_service,
        tenant_service=tenant_service
    )
