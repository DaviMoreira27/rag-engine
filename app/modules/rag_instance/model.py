from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import Boolean, Integer
from uuid import uuid4

from app.core.database import BaseModel

if TYPE_CHECKING:
    from app.modules.tenant.model import Tenant

class RAGInstance(BaseModel):
    __tablename__ = "rag_instances"
    rag_id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    tenant_id: Mapped[str] = mapped_column(ForeignKey('tenants.tenant_id'))
    name: Mapped[str] = mapped_column(String(100))
    llm_provider: Mapped[str] = mapped_column(String(50))
    llm_model: Mapped[str] = mapped_column(String(100))
    chunk_size: Mapped[int] = mapped_column(Integer, default=1024)
    chunk_overlap: Mapped[int] = mapped_column(Integer, default=128)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tenant: Mapped[Tenant] = relationship(back_populates='rag_instances')
