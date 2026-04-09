from fastapi import APIRouter, Depends, status

from app.modules.auth.dependency import get_auth_service
from app.modules.auth.service import AuthService
from app.modules.user.schema import (
    LoginRequest,
    LoginResponse,
    SignupRequest,
    SignupResponse,
)
from app.modules.user.exception import UserNotFoundError, UserAlreadyExistsError
from app.modules.auth.schema import CreateUserRequest, UserCreationTenantData

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    """Login with email and password, returns a session ID."""
    session_id = await auth_service.login(request.email, request.password)
    user = await auth_service._user_service.get_user_by_email(request.email)

    if not user:
        raise UserNotFoundError("User not found")

    return LoginResponse(
        session_id=session_id,
        user_id=str(user.user_id),
        tenant_id=str(user.tenant_id),
    )


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> SignupResponse:
    """Create a new user account and return a session ID."""
    create_user_request = CreateUserRequest(
        name=request.name,
        email=request.email,
        password=request.password,
        tenant=UserCreationTenantData(
            tenant_id=request.tenant_id,
            name=request.name,
        ),
    )

    session_id = await auth_service.sign_up(create_user_request)
    user = await auth_service._user_service.get_user_by_email(request.email)

    if not user:
        raise UserNotFoundError("User creation failed")

    return SignupResponse(
        session_id=session_id,
        user_id=str(user.user_id),
        tenant_id=str(user.tenant_id),
        email=user.email,
        name=user.name,
    )
