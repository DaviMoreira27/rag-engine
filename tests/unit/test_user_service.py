import pytest
from unittest.mock import AsyncMock
from app.modules.user.exception import UserAlreadyExistsError
from app.modules.user.model import User
from tests.factories import UserFactory


async def test_create_user_returns_correct_response(user_service, mock_user_repository):
    user = UserFactory()
    mock_user_repository.create_user.return_value = user

    response = await user_service.create_user(
        email=user.email,
        password_hash=user.password_hash,
        tenant_id=user.tenant_id,
        name=user.name,
    )

    assert response.email == user.email
    assert response.user_id == str(user.user_id)
    assert response.tenant_id == str(user.tenant_id)


async def test_create_user_passes_correct_user_to_repo(user_service, mock_user_repository):
    user = UserFactory()
    mock_user_repository.create_user.return_value = user

    await user_service.create_user(
        email=user.email,
        password_hash=user.password_hash,
        tenant_id=user.tenant_id,
        name=user.name,
    )

    call_args = mock_user_repository.create_user.call_args
    created: User = call_args.args[0]
    assert created.email == user.email
    assert created.tenant_id == user.tenant_id
    assert created.name == user.name
    assert created.is_active is True


async def test_get_user_by_email_delegates_to_repo(user_service, mock_user_repository):
    user = UserFactory()
    mock_user_repository.get_user_by_email.return_value = user

    result = await user_service.get_user_by_email(user.email)

    mock_user_repository.get_user_by_email.assert_called_once_with(user.email)
    assert result == user


async def test_get_user_by_email_returns_none_when_not_found(user_service, mock_user_repository):
    mock_user_repository.get_user_by_email.return_value = None

    result = await user_service.get_user_by_email("notfound@example.com")

    assert result is None


async def test_ensure_email_not_taken_raises_when_user_exists(user_service, mock_user_repository):
    user = UserFactory()
    mock_user_repository.get_user_by_email.return_value = user

    with pytest.raises(UserAlreadyExistsError):
        await user_service.ensure_email_not_taken(user.email)


async def test_ensure_email_not_taken_passes_when_no_user(user_service, mock_user_repository):
    mock_user_repository.get_user_by_email.return_value = None

    await user_service.ensure_email_not_taken("free@example.com")
