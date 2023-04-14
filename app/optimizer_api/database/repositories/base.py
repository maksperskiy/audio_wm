from sqlalchemy.future import select
from app.optimizer_api.api.middlewares import db_session


class BaseRepository:
    __model__ = None

    @staticmethod
    async def execute(query, flush: bool = False):
        result = await db_session.get().execute(query)
        if flush:
            await db_session.get().flush()
        return result

    @staticmethod
    async def flush() -> None:
        await db_session.get().flush()

    @classmethod
    async def get(cls, **params) -> __model__:
        if not cls.__model__:
            raise NotImplementedError("BaseRepository hasn't this method")
        query = select(cls.__model__).filter_by(**params)
        result = await cls.execute(query)
        return result.scalars().first()

    @classmethod
    async def create(cls, entity: __model__) -> __model__:
        db_session.get().add(entity)
        await cls.flush()
        return entity

    @classmethod
    async def update(cls, updates: dict, **params) -> __model__:
        if not cls.__model__:
            raise NotImplementedError("BaseRepository hasn't this method")
        query = select(cls.__model__).filter_by(**params)
        result = await cls.execute(query)
        entity = result.scalars().first()
        for field, data in updates.items():
            setattr(entity, field, data)
        await cls.flush()
        return entity
