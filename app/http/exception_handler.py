"""HTTP exception handlers - maps domain exceptions to HTTP responses"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from app.core.exceptions import (
    AppException,
    InfrastructureException,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    UnprocessableEntityError,
    ExternalServiceException,
)

logger = logging.getLogger(__name__)

# Domain exceptions to HTTP status codes
_DOMAIN_TO_HTTP = {
    BadRequestError: 400,
    UnauthorizedError: 401,
    ForbiddenError: 403,
    NotFoundError: 404,
    ConflictError: 409,
    UnprocessableEntityError: 422,
}

# Infrastructure exceptions to HTTP status codes
_INFRA_TO_HTTP = {
    ExternalServiceException: 502,
    InfrastructureException: 500,  # fallback
}


def resolve_status_code(exc: Exception) -> int:
    """Resolve exception to HTTP status code"""
    # Check domain exceptions
    for exc_type, status in _DOMAIN_TO_HTTP.items():
        if isinstance(exc, exc_type):
            return status

    # Check infrastructure exceptions
    for exc_type, status in _INFRA_TO_HTTP.items():
        if isinstance(exc, exc_type):
            return status

    return 500


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle business logic exceptions"""
    status_code = resolve_status_code(exc)

    logger.error(
        f"Business logic error: {exc.error_code}",
        extra={"error_code": exc.error_code, "message": exc.message},
        exc_info=exc,
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
        },
    )


async def infrastructure_exception_handler(
    request: Request, exc: InfrastructureException
) -> JSONResponse:
    """Handle infrastructure/technical exceptions"""
    status_code = resolve_status_code(exc)

    logger.error(
        f"Infrastructure error: {exc.error_code}",
        extra={"error_code": exc.error_code},
        exc_info=exc,
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": exc.error_code,
            "message": "Internal server error",
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    logger.critical(
        "Unhandled exception",
        extra={"error_type": type(exc).__name__},
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Internal server error",
        },
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI app"""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(InfrastructureException, infrastructure_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
