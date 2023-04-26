import csv
import os
import random
from typing import List, Union

import numpy as np
from scipy.io import wavfile

from app.optimizer_api.database.audio_provider.abstract_provider import AbstractProvider
from app.optimizer_api.exceptions import NotFoundException


class FileProvider(AbstractProvider):
    labels_tree = []
    with open(
        "/app/optimizer_api/api/handlers/audio/classes_tree.csv", newline=""
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for i in range(6):
                labels_tree.append([i for i in row.values()])
    labels = [item for sublist in labels_tree for item in sublist]
    labels = ["Animal", "Music", "Speech", "Dog"]
    labels = list(sorted(set(labels)))

    @classmethod
    def get_label_children(cls, label: str):
        labels = []
        for labels_group in cls.labels_tree:
            for i in range(6):
                if labels_group[i] == label:
                    labels.extend(
                        [
                            labels_group[j]
                            for j in range(i, 6)
                            if labels_group[j] and labels_group[j] not in labels
                        ]
                    )
        return labels

    @classmethod
    async def get_random_audio(cls, label: str = None) -> Union[np.ndarray, int]:
        audio_folder = "./data/fold2/"

        files = [
            os.path.join(audio_folder, f)
            for f in os.listdir(audio_folder)
            if os.path.isfile(os.path.join(audio_folder, f))
        ]

        if label:
            labels = cls.get_label_children(label)
            files = list(filter(lambda x: any([el in x for el in labels]), files))

        if not files:
            raise NotFoundException

        file_path = random.choice(files)

        rate, data = wavfile.read(file_path)

        return data, rate
