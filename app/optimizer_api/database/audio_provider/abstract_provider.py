from abc import ABCMeta, abstractclassmethod

from typing import Union
import numpy as np


class AbstractProvider(metaclass=ABCMeta):
    @abstractclassmethod
    async def get_random_audio(cls, label: str = None) -> Union[np.ndarray, int]:
        pass
