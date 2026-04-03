import pytest_asyncio as aiopytest
from unittest.mock import AsyncMock
from app.modules.session.service import SessionService
from tests.factories import UserFactory

@aiopytest.fixture
async def mock_repository():
    repo = AsyncMock()
    repo.get.return_value = {"user_id": "user1", "tenant_id": "tenant1"}
    repo.get_set_members.return_value = {"session:abc123", "session:def456"}
    return repo

@aiopytest.fixture
async def session_service(mock_repository):
    return SessionService(session_repository=mock_repository, ttl=3600)

async def test_create_session_calls_save_with_correct_set_key(session_service, mock_repository):
    user = UserFactory()
    session_id = await session_service.create_session(user)

    mock_repository.save.assert_called_once_with(
        session_id=session_id,
        data={"user_id": str(user.user_id), "tenant_id": str(user.tenant_id)},
        ttl=3600,
        set_key=f"tenant_sessions:{user.tenant_id}"
    )

async def test_bulk_remove_calls_remove_for_each_session(session_service, mock_repository):
    await session_service.bulk_remove_by_tenant("tenant1")

    mock_repository.get_set_members.assert_called_once_with("tenant_sessions:tenant1")
    assert mock_repository.remove.call_count == 2

async def test_create_session_returns_valid_session_id(session_service, mock_repository):
    user = UserFactory()
    session_id = await session_service.create_session(user)

    assert session_id is not None
    assert len(session_id) > 0

    call_args = mock_repository.save.call_args
    assert call_args.kwargs["data"]["user_id"] == str(user.user_id)
    assert call_args.kwargs["data"]["tenant_id"] == str(user.tenant_id)
    assert call_args.kwargs["ttl"] == 3600
    assert call_args.kwargs["set_key"] == f"tenant_sessions:{user.tenant_id}"
