import functools
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from app.ai_api.database.core import async_session_factory

db_session: ContextVar[AsyncSession] = ContextVar("db-session")


def in_session(*, commit: bool = False):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_session_factory("AI") as session_:
                db_session.set(session_)
                response = await func(*args, **kwargs)
                if commit:
                    await db_session.get().commit()
            return response

        return wrapper

    return decorator
