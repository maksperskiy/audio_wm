from typing import List

from fastapi import APIRouter, Depends, Query

from app.optimizer_api.api.handlers.export import ExportHandler
from app.optimizer_api.api.middlewares import in_session

router = APIRouter()


@router.get("/")
@in_session(commit=True)
async def get_sound(
    labels: List[str] = Query(None),
    Export_handler: ExportHandler = Depends(),
):
    return await Export_handler.export(labels)
