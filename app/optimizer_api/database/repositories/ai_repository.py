from typing import List
from sqlalchemy.future import select
from sqlalchemy import delete

from app.optimizer_api.database.models import ParamsModel
from app.optimizer_api.database.repositories.base import BaseRepository

from app.optimizer_api.api.middlewares import db_ai_session


class AIRepository(BaseRepository):
    __model__ = ParamsModel
    db_session = db_ai_session

    @classmethod
    async def delete_old_params(cls, labels: List[str]) -> __model__:
        query = delete(cls.__model__).filter(cls.__model__.label.in_(labels))
        await cls.execute(query, flush=True)
