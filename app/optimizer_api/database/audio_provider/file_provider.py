from typing import List, Union
import csv
import numpy as np
import os
from scipy.io import wavfile
import random

from app.optimizer_api.exceptions import NotFoundException

from app.optimizer_api.database.audio_provider.abstract_provider import AbstractProvider


class FileProvider(AbstractProvider):
    @classmethod
    async def get_labels(cls) -> List[str]:
        labels = []
        with open(
            "/app/optimizer_api/api/handlers/audio/classes_tree.csv", newline=""
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for i in range(6):
                    labels.append(row[f"{i}"])

        return list(sorted(set(labels)))

    @classmethod
    async def get_random_audio(cls, label: str = None) -> Union[np.ndarray, int]:
        audio_folder = "./data/fold2/"

        files = [
            os.path.join(audio_folder, f)
            for f in os.listdir(audio_folder)
            if os.path.isfile(os.path.join(audio_folder, f))
        ]

        if label:
            files = list(filter(lambda x: label in x, files))

        if not files:
            raise NotFoundException

        file_path = random.choice(files)

        rate, data = wavfile.read(file_path)

        return data, rate
