from typing import List, Any

from app.optimizer_api.schemas.responses.base import BaseResponse


class LabelsResponse(BaseResponse):
    labels: List[str]


class SoundResponse(BaseResponse):
    label: str
    message: bytes
    extracted_message: bytes

    sound_array: List[Any]
    injected_sound_array: List[Any]
    samplerate: int

    sound_noise_ratio: float
    success_ratio: float
