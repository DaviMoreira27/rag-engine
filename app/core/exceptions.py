"""Domain exceptions - no HTTP semantics, purely domain logic"""


class AppException(Exception):
    """Base exception for all business logic errors"""

    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


# Business Logic Errors
class BadRequestError(AppException):
    """Validation of input failed"""
    pass


class UnauthorizedError(AppException):
    """Not authenticated (invalid credentials)"""
    pass


class ForbiddenError(AppException):
    """Authenticated but without permission"""
    pass


class NotFoundError(AppException):
    """Resource does not exist"""
    pass


class ConflictError(AppException):
    """Conflict of state (duplicate, invalid transition)"""
    pass


class UnprocessableEntityError(AppException):
    """Semantic validation failed"""
    pass


# Infrastructure Errors
class InfrastructureException(Exception):
    """Base exception for infrastructure/technical errors"""

    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class DatabaseException(InfrastructureException):
    """Database connection or query error"""
    pass


class ExternalServiceException(InfrastructureException):
    """External service unavailable"""
    pass


class InternalServerException(InfrastructureException):
    """Unexpected internal error"""
    pass
