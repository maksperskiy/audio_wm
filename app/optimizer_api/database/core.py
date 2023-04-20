from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.optimizer_api.core import settings


_async_optimizer_engine = create_async_engine(
    settings.DATABASE_OPTIMIZER_URI,
    echo=False,
    query_cache_size=0,
)
_async_optimizer_session = sessionmaker(
    _async_optimizer_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)

_async_ai_engine = create_async_engine(
    settings.DATABASE_AI_URI,
    echo=False,
    query_cache_size=0,
)
_async_ai_session = sessionmaker(
    _async_ai_engine, expire_on_commit=False, class_=AsyncSession, autoflush=False
)


@asynccontextmanager
async def async_session_factory(
    database: str = None,
) -> Callable[..., AbstractContextManager[AsyncSession]]:
    if database == "AI":
        session_ = _async_ai_session()
    else:
        session_ = _async_optimizer_session()

    try:
        yield session_
    except Exception:
        await session_.rollback()
        raise
    finally:
        await session_.close()
