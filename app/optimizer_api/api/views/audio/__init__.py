from fastapi import APIRouter, Depends

from .audio import router as audio_router


router = APIRouter(
    prefix="/audio", 
)

router.include_router(audio_router)
