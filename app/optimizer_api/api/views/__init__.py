from fastapi import APIRouter

from app.optimizer_api.api.views.audio import router as audio_router
from app.optimizer_api.core import Constants


router = APIRouter(prefix=Constants.APP_PREFIX)

router.include_router(audio_router, tags=["audio"])
