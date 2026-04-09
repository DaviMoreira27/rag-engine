from abc import abstractmethod, ABC
from .model import User

class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def create_user(self, user: User) -> User: ...
