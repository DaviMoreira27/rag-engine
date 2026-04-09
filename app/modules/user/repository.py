from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.modules.user.interface import UserRepository

from .model import User

class UserRepositoryImpl(UserRepository):
    def __init__(self, database: AsyncSession):
        self.db = database

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()  # sends the INSERT command but does not commit
        await self.db.refresh(user)  # updates the object with the auto generated fields
        return user
