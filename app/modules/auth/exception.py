from app.core.exceptions import UnauthorizedError


class InvalidCredentialsError(UnauthorizedError):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, "INVALID_CREDENTIALS")
