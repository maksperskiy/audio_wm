from typing import List

from sqlalchemy.future import select

from app.ai_api.api.middlewares import db_session


class BaseRepository:
    __model__ = None

    @classmethod
    async def execute(cls, query, flush: bool = False):
        result = await db_session.get().execute(query)
        if flush:
            await db_session.get().flush()
        return result

    @classmethod
    async def flush(cls) -> None:
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
    async def bulk_create(cls, entities: List[__model__]) -> List[__model__]:
        db_session.get().add_all(entities)
        await cls.flush()
        return entities

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
