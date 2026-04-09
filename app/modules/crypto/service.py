from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

from app.modules.auth.exception import InvalidCredentialsError
from app.modules.crypto.interface import CryptoServicePort

class ArgonCryptoService(CryptoServicePort):
    def __init__(self, hasher: PasswordHasher) -> None:
        self._hasher = hasher

    def hash(self, plain_text: str) -> str:
        return self._hasher.hash(plain_text)

    def verify(self, hashed: str, plain_text: str) -> bool:
        try:
            return self._hasher.verify(hashed, plain_text)

        except InvalidHashError:
            raise InvalidCredentialsError("Invalid hash or corrupted")
        except VerifyMismatchError:
            return False
