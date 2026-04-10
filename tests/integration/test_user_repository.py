from uuid import uuid4
from app.modules.user.model import User
from app.modules.user.repository import UserRepositoryImpl
from app.modules.tenant.model import Tenant


async def _insert_tenant(db_session) -> Tenant:
    tenant = Tenant(tenant_id=str(uuid4()), name="Test Tenant", is_active=True)
    db_session.add(tenant)
    await db_session.flush()
    return tenant


def _make_user(tenant_id: str) -> User:
    return User(
        user_id=str(uuid4()),
        tenant_id=tenant_id,
        name="John Doe",
        email=f"{uuid4()}@example.com",
        password_hash="hashed",
        is_active=True,
    )


async def test_create_user_persists_and_returns_user(db_session):
    tenant = await _insert_tenant(db_session)
    repo = UserRepositoryImpl(database=db_session)
    user = _make_user(tenant.tenant_id)

    created = await repo.create_user(user)

    assert created.user_id == user.user_id
    assert created.email == user.email
    assert created.tenant_id == tenant.tenant_id


async def test_get_user_by_email_returns_user(db_session):
    tenant = await _insert_tenant(db_session)
    repo = UserRepositoryImpl(database=db_session)
    user = _make_user(tenant.tenant_id)
    await repo.create_user(user)

    found = await repo.get_user_by_email(user.email)

    assert found is not None
    assert found.user_id == user.user_id


async def test_get_user_by_email_returns_none_when_not_found(db_session):
    repo = UserRepositoryImpl(database=db_session)

    result = await repo.get_user_by_email("nonexistent@example.com")

    assert result is None
