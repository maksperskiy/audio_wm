from app.optimizer_api.schemas.requests.base import BaseRequest


class EstimationRequest(BaseRequest):
    label: str

    expert_score: int
    sound_noise_ratio: float
    success_ratio: float
