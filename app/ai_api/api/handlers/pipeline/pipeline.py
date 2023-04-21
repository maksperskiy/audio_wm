import base64
import csv
import json

import numpy as np
import requests
import scipy.signal as sps
from spleeter.separator import Separator

from app.ai_api.core import settings
from app.ai_api.database.repositories import AIRepository
from app.ai_api.schemas.requests.audio import AudioRequest
from app.ai_api.schemas.responses.params import ParamsResponse


class PipelineHandler:
    @staticmethod
    async def resample(audio: np.ndarray, samplerate: int) -> np.ndarray:
        number_of_samples = round(len(audio) * float(16000) / samplerate)
        data = sps.resample(audio, number_of_samples)
        return data.astype(np.int16)

    @classmethod
    async def classify(cls, audio: np.ndarray, samplerate: int) -> str:
        audio = await cls.resample(audio, samplerate)
        result = requests.post(
            f"{settings.CLASSIFIER_URI}/v1/models/classifier:predict",
            data=json.dumps({"inputs": audio.tolist()}),
        )
        if result:
            labels = {}
            with open(
                "/app/ai_api/api/handlers/pipeline/assets/yamnet_class_map.csv",
                newline="",
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    labels[int(row["index"])] = row["display_name"]

            return labels.get(
                np.array(json.loads(result.content)["outputs"]["output_0"]).argmax()
            )

    @staticmethod
    async def separate(audio: np.ndarray) -> dict:
        audio = np.column_stack((audio, audio)).astype(np.float32) / 32768
        separator = Separator(
            "spleeter:2stems", stft_backend="librosa", multiprocess=True
        )
        prediction = separator.separate(audio)
        return (
            prediction["vocals"][:, 0] * 32768,
            prediction["accompaniment"][:, 0] * 32768,
        )

    @classmethod
    async def get_params(
        cls,
        request: AudioRequest,
    ) -> ParamsResponse:
        audio = np.frombuffer(base64.decodebytes(request.audio), dtype=np.int16)

        if request.spleeter:
            _, audio = await cls.separate(audio)

        label = await cls.classify(audio, request.samplerate)

        params = await AIRepository.get(label=label)
        if not params:
            params = ParamsResponse(
                label=label, freq_bottom=1750, freq_top=8500, duration=20
            )
        return params
