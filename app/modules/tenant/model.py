from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import Boolean
from uuid import uuid4

from app.database import BaseModel

if TYPE_CHECKING:
    from app.modules.user.model import User

class Tenant(BaseModel):
    __tablename__ = "tenants"
    tenant_id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    users: Mapped[List[User]] = relationship(back_populates='tenant')
