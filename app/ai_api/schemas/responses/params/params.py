from typing import Optional
from app.ai_api.schemas.responses.base import BaseResponse

from datetime import datetime


class ParamsResponse(BaseResponse):
    label: str
    message: Optional[bytes]

    freq_bottom: int
    freq_top: int
    duration: int

    created_at: datetime
