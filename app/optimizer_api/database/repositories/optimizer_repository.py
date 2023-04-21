from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.optimizer_api.api.middlewares import db_optimizer_session
from app.optimizer_api.database.models import ParamsHistoryModel
from app.optimizer_api.database.repositories.base import BaseRepository


class OptimizerRepository(BaseRepository):
    __model__ = ParamsHistoryModel
    db_session = db_optimizer_session

    @classmethod
    async def get_last_params(
        cls,
        label: str,
    ) -> __model__:
        query = (
            select(cls.__model__)
            .filter_by(label=label)
            .order_by(cls.__model__.created_at.desc())
            .limit(1)
        )
        result = await cls.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_last_base_params(
        cls,
        label: str,
    ) -> __model__:
        query = (
            select(cls.__model__)
            .filter_by(label=label, param_number=None)
            .order_by(cls.__model__.created_at.desc())
            .limit(1)
        )
        result = await cls.execute(query)
        return result.scalars().first()

    @classmethod
    async def intialize_params(
        cls,
        label,
        experiment_number=0,
        freq_bottom=None,
        freq_top=None,
        duration=None,
        freq_bottom_step=None,
        freq_top_step=None,
        duration_step=None,
    ):
        params = ParamsHistoryModel(
            step_number=0,
            label=label,
            experiment_number=experiment_number,
            freq_bottom=freq_bottom or 1750,
            freq_top=freq_top or 8500,
            duration=duration or 20,
            freq_bottom_step=freq_bottom_step or 10000,
            freq_top_step=freq_top_step or 10000,
            duration_step=duration_step or 10000,
        )
        await cls.create(params)
        return params
