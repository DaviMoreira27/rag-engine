import factory
from uuid import uuid4

from factory.declarations import LazyFunction
from app.modules.user.model import User
from app.modules.tenant.model import Tenant

class TenantFactory(factory.base.Factory):
    class Meta:  # type: ignore[override] - factory-boy overrides Meta by design, Pyright incorrectly flags this as a type error
        model = Tenant

    tenant_id = LazyFunction(lambda: str(uuid4()))
    name = factory.faker.Faker("company")
    is_active = True

class UserFactory(factory.base.Factory):
    class Meta:  # type: ignore[override] - factory-boy overrides Meta by design, Pyright incorrectly flags this as a type error
        model = User

    user_id = LazyFunction(lambda: str(uuid4()))
    tenant_id = LazyFunction(lambda: str(uuid4()))
    name = factory.faker.Faker("name")
    email = factory.faker.Faker("email")
    password_hash = "hashed_password"
    is_active = True
