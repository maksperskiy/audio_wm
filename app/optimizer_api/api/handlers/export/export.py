from typing import List

from app.optimizer_api.database.models import ParamsModel

from app.optimizer_api.database.repositories import OptimizerRepository
from app.optimizer_api.database.repositories import AIRepository


class ExportHandler:
    @staticmethod
    async def export(labels: List[str]):
        params = []
        for label in labels:
            params.append(await OptimizerRepository.get_last_base_params(label))
        await AIRepository.delete_old_params(labels)
        new_params = [
            ParamsModel(
                label=el.label,
                freq_bottom=el.freq_bottom,
                freq_top=el.freq_top,
                duration=el.duration,
            )
            for el in params
        ]
        await AIRepository.bulk_create(new_params)
