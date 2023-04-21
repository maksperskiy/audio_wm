from app.ai_api.schemas.requests.base import BaseRequest


class AudioRequest(BaseRequest):
    audio: bytes
    samplerate: int
    spleeter: bool = False
