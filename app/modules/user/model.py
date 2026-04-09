from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import Boolean
from uuid import uuid4

from app.core.database import BaseModel

if TYPE_CHECKING:
    from app.modules.tenant.model import Tenant

class User(BaseModel):
    __tablename__ = "users"
    user_id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    tenant_id: Mapped[str] = mapped_column(ForeignKey('tenants.tenant_id'))
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    password_hash: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    tenant: Mapped[Tenant] = relationship(back_populates='users')
