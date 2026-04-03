from typing import AsyncGenerator, ClassVar
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.orm.base import Mapped
from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Config

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class BaseModel(TimestampMixin, Base):
    __abstract__ = True
    __repr_exclude__: ClassVar[set[str]] = set()

    def __repr__(self) -> str:
        cols = ", ".join(
            f"{col.key}={getattr(self, col.key)!r}"
            for col in self.__table__.columns
            if col.key not in self.__repr_exclude__
        )
        return f"{self.__class__.__name__}({cols})"

config = Config()

engine = create_async_engine(
    config.get_database_connection_url(),  # postgresql+asyncpg://user:pass@host/db
    pool_size=10, # number of open connections permanently in the pool.
    max_overflow=20, # extra connections permitted for high access momments. They are closed when the burst seizes
    pool_pre_ping=True,   # checks if the database is ready to receive connections
    pool_recycle=3600,    # discards connections after 1 hour, preveting zombie connections
    # (postgres already closed them but the system still thinks they are ready)
    echo=False,          # SQL logging for debugging and dev envs
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,     # which engine will use to create sessions
    class_=AsyncSession, # indicates to use the async version of Sessions to the SQL Alchemy
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            if session.is_active:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
