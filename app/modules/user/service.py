from app.modules.user.exception import UserAlreadyExistsError
from app.modules.user.interface import UserRepository
from app.modules.user.schema import UserCreationResponse
from app.modules.user.model import User

from uuid import uuid4

class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repo.get_user_by_email(email)

    async def create_user(self, email: str, password_hash: str, tenant_id:  str, name: str) -> UserCreationResponse:
        user = User(
            user_id=str(uuid4()),
            tenant_id=tenant_id,
            email=email,
            password_hash=password_hash,
            name=name,
            is_active=True,
        )
        created = await self.repo.create_user(user)
        return UserCreationResponse(
            user_id=str(created.user_id),
            email=created.email,
            tenant_id=str(created.tenant_id),
        )

    async def ensure_email_not_taken(self, email: str) -> None:
        user = await self.repo.get_user_by_email(email)
        if user:
            raise UserAlreadyExistsError("Email already in use")
