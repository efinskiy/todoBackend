from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy import func, TIMESTAMP
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from app.config import DB_URL

async_engine: AsyncEngine = create_async_engine(
    url=DB_URL,
    pool_size=10,
    max_overflow=20,
)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# Генератор сессии SQLAlchemy для использования в Depends()
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    # Базовый класс для моделей SQLAlchemy.

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )

    # Устанавливаем дефолтное название таблиц на название модели lowercase'ом.
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
