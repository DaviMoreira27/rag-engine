from app.core.exceptions import ConflictError, NotFoundError


class UserNotFoundError(NotFoundError):
    def __init__(self, message: str = "User not found"):
        super().__init__(message, "USER_NOT_FOUND")


class UserAlreadyExistsError(ConflictError):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, "USER_ALREADY_EXISTS")
