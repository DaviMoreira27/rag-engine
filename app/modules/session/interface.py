from abc import ABC, abstractmethod

class SessionRepository(ABC):
    @abstractmethod
    async def save(self, session_id: str, data: dict, ttl: int, set_key: str) -> None: ...

    @abstractmethod
    async def get(self, session_id: str) -> dict | None: ...

    @abstractmethod
    async def remove(self, session_id: str) -> None: ...

    @abstractmethod
    async def get_set_members(self, key: str) -> set[str]: ...
