from fastapi import APIRouter, Depends

from .pipeline import router as pipeline_router


router = APIRouter(
    prefix="/pipeline", 
)

router.include_router(pipeline_router)
