import pytest
from unittest.mock import AsyncMock
from app.modules.session.service import SessionService


@pytest.fixture
async def mock_repository():
    repo = AsyncMock()
    repo.get.return_value = {"user_id": "user1", "tenant_id": "tenant1"}
    repo.get_set_members.return_value = {"session:abc123", "session:def456"}
    return repo


@pytest.fixture
async def session_service(mock_repository):
    return SessionService(session_repository=mock_repository, ttl=3600)
