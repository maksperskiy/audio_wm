import functools
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from app.optimizer_api.database.core import async_session_factory

db_optimizer_session: ContextVar[AsyncSession] = ContextVar("optimizer-db-session")
db_ai_session: ContextVar[AsyncSession] = ContextVar("ai-db-session")


def in_session(*, commit: bool = False):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_session_factory("AI") as ai_session_:
                async with async_session_factory("optimizer") as optimizer_session_:
                    db_ai_session.set(ai_session_)
                    db_optimizer_session.set(optimizer_session_)
                    response = await func(*args, **kwargs)
                    if commit:
                        await db_ai_session.get().commit()
                        await db_optimizer_session.get().commit()
            return response

        return wrapper

    return decorator
