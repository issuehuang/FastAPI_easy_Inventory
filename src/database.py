from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from src.utils import generate_uuid

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./example.db"

# initial db engine
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# initial session maker
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    id = mapped_column(String, primary_key=True, default=generate_uuid)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )


# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
