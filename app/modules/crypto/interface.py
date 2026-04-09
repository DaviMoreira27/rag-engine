from abc import abstractmethod, ABC

class CryptoServicePort(ABC):
    @abstractmethod
    def hash(self, plain_text: str) -> str: ...

    @abstractmethod
    def verify(self, hashed: str, plain_text: str) -> bool: ...
