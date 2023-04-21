from fastapi import APIRouter, Depends

from app.ai_api.api.middlewares import in_session

from app.ai_api.api.handlers.pipeline import PipelineHandler

from app.ai_api.schemas.requests.audio import AudioRequest
from app.ai_api.schemas.responses.params import ParamsResponse


router = APIRouter()


@router.post("/", response_model=ParamsResponse)
@in_session()
async def get_sound(
    audio: AudioRequest,
    pipeline_handler: PipelineHandler = Depends(),
):
    return await pipeline_handler.get_params(audio)
