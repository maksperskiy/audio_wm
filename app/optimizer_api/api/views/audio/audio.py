from fastapi import APIRouter, Depends, Query

from app.optimizer_api.api.handlers.audio import AudioHandler
from app.optimizer_api.api.middlewares import in_session
from app.optimizer_api.schemas.requests.audio import EstimationRequest
from app.optimizer_api.schemas.responses.audio import LabelsResponse, SoundResponse

router = APIRouter()


@router.get("/labels/", response_model=LabelsResponse)
@in_session()
async def get_sound(
    audio_handler: AudioHandler = Depends(),
):
    return await audio_handler.get_labels()


@router.get("/", response_model=SoundResponse)
@in_session(commit=True)
async def get_sound(
    label: str = Query(None),
    audio_handler: AudioHandler = Depends(),
):
    return await audio_handler.get_audio(label)


@router.post("/estimate/")
@in_session(commit=True)
async def get_sound(
    estimation: EstimationRequest,
    audio_handler: AudioHandler = Depends(),
):
    await audio_handler.optimize(estimation)


@router.get("/reset/")
@in_session(commit=True)
async def get_sound(
    label: str = Query(None),
    audio_handler: AudioHandler = Depends(),
):
    await audio_handler.reset_label(label)
