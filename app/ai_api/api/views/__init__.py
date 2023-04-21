from fastapi import APIRouter

from app.ai_api.api.views.pipeline import router as pipeline_router
from app.ai_api.core import Constants


router = APIRouter(prefix=Constants.APP_PREFIX)

router.include_router(pipeline_router, tags=["pipeline"])
