from argon2 import PasswordHasher
from fastapi import Depends

from app.modules.crypto.service import ArgonCryptoService


def get_hasher() -> PasswordHasher:
    return PasswordHasher(
        time_cost=2,
        memory_cost=19456,
        parallelism=1,
    )

def get_crypto_service(
    hasher: PasswordHasher = Depends(get_hasher)
) -> ArgonCryptoService:
    return ArgonCryptoService(hasher)
