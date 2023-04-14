from app.optimizer_api.exceptions import NotFoundException, BadRequestException

from app.optimizer_api.database.repositories import FileRepository
from app.optimizer_api.database.repositories import OptimizerRepository

from app.optimizer_api.database.models import ParamsModel

from app.optimizer_api.schemas.requests.audio import EstimationRequest
from app.optimizer_api.schemas.responses.audio import SoundResponse, LabelsResponse

from app.optimizer_api.core.injector import Injector, Extractor

import numpy as np


class AudioHandler:
    @staticmethod
    async def get_labels():
        labels = await FileRepository.get_labels()

        return LabelsResponse(labels=labels)

    @staticmethod
    async def get_audio(label: str):
        sound, samplerate = await FileRepository.get_random_audio(label)
        params = await OptimizerRepository.get_last_params(label)
        
        if not params:
            params = await OptimizerRepository.intialize_params(label=label)

        if sound.dtype == 'int32':
            sound = (sound>>16).astype(np.int16)

        injector = Injector(
            message=0x123456,
            bottom_freq=params.freq_bottom,
            top_freq=params.freq_top,
            duration=params.duration,
        )
        injected_sound, _, _, _, sound_noise_ratio = injector.process(sound, samplerate)

        extractor = Extractor(
            bottom_freq=params.freq_bottom,
            top_freq=params.freq_top,
            duration=params.duration,
        )
        message, success_ratio = extractor.process(injected_sound, samplerate)

        result = SoundResponse(
            label=label,
            message=0x123456,
            extracted_message=message,
            sound_array=sound.tolist(),
            injected_sound_array=injected_sound.tolist(),
            samplerate=samplerate,
            sound_noise_ratio=sound_noise_ratio,
            success_ratio=success_ratio,
        )
        return result

    @staticmethod
    async def __limit_value(value, min_value=0, max_value=20000):
        if value > max_value:
            return max_value
        elif value < min_value:
            return min_value
        return value

    @staticmethod
    async def __count_reward(expert_score, sound_noise_ratio, success_ratio):
        return expert_score / 5 + 1 / sound_noise_ratio + success_ratio

    @classmethod
    async def optimize(
        cls,
        estimation: EstimationRequest,
    ) -> None:
        last_params = await OptimizerRepository.get_last_params(estimation.label)
        base_params = await OptimizerRepository.get_last_base_params(estimation.label)

        base_reward = cls.__count_reward(
            base_params.expert_score,
            base_params.sound_noise_ratio,
            base_params.success_ratio,
        )
        reward = cls.__count_reward(
            estimation.expert_score,
            estimation.sound_noise_ratio,
            estimation.success_ratio,
        )

        if last_params.param_number == None:
            # set to base reward
            # create new params with stepped freq_b
            params = {
                "label": base_reward.label,
                "step_number": base_reward.step_number,
            }
            updates = {
                "expert_score": estimation.expert_score,
                "sound_noise_ratio": estimation.sound_noise_ratio,
                "success_ratio": estimation.success_ratio,
            }
            await OptimizerRepository.update(updates=updates, params=params)

            new_params = ParamsModel(
                step_number=last_params.step_number + 1,
                label=estimation.label,
                param_number=0,
                freq_bottom=cls.__limit_value(
                    base_params.freq_bottom + base_params.freq_bottom_step,
                    max_value=base_params.freq_top - 1,
                ),
                freq_top=base_params.freq_top,
                duration=base_params.duration,
                freq_bottom_step=base_params.freq_bottom_step,
                freq_top_step=base_params.freq_top_step,
                duration_step=base_params.duration_step,
            )
            await OptimizerRepository.create(new_params)

        elif last_params.param_number == 0:
            # set to base freq_b grad
            # create new params with stepped freq_t
            gradient = reward - base_reward
            params = {
                "label": base_reward.label,
                "step_number": base_reward.step_number,
            }
            updates = {
                "freq_bottom_grad": gradient,
            }
            await OptimizerRepository.update(updates=updates, params=params)

            new_params = ParamsModel(
                step_number=last_params.step_number + 1,
                label=estimation.label,
                param_number=1,
                freq_bottom=base_params.freq_bottom,
                freq_top=cls.__limit_value(
                    base_params.freq_top + base_params.freq_top_step,
                    min_value=base_params.freq_bottom + 1,
                ),
                duration=base_params.duration,
                freq_bottom_step=base_params.freq_bottom_step,
                freq_top_step=base_params.freq_top_step,
                duration_step=base_params.duration_step,
            )
            await OptimizerRepository.create(new_params)

        elif last_params.param_number == 1:
            # set to base freq_t grad
            # create new params with stepped duration
            gradient = reward - base_reward
            params = {
                "label": base_reward.label,
                "step_number": base_reward.step_number,
            }
            updates = {
                "freq_top_grad": gradient,
            }
            await OptimizerRepository.update(updates=updates, params=params)

            new_params = ParamsModel(
                step_number=last_params.step_number + 1,
                label=estimation.label,
                param_number=2,
                freq_bottom=base_params.freq_bottom,
                freq_top=base_params.freq_top,
                duration=cls.__limit_value(
                    base_params.duration + base_params.duration_step,
                    min_value=10,
                    max_value=975,
                ),
                freq_bottom_step=base_params.freq_bottom_step,
                freq_top_step=base_params.freq_top_step,
                duration_step=base_params.duration_step,
            )
            await OptimizerRepository.create(new_params)

        elif last_params.param_number == 2:
            # set to base duration grad
            gradient = reward - base_reward
            params = {
                "label": base_reward.label,
                "step_number": base_reward.step_number,
            }
            updates = {
                "duration_grad": gradient,
            }
            await OptimizerRepository.update(updates=updates, params=params)
            # create new base with updated params, steps, empty param_number, reward and grads
            # reset steps if step_number more that xx

            if last_params.step_number % 28 == 4 and last_params.step_number // 84 >= 1:
                new_freq_bottom_step = 100
                new_freq_top_step = 100
                new_duration_step = 100
            else:
                new_freq_bottom_step = (
                    base_params.freq_bottom_step / 2
                    if base_params.freq_bottom_grad < 0
                    else base_params.freq_bottom_step
                )
                new_freq_top_step = (
                    base_params.freq_top_step / 2
                    if base_params.freq_top_grad < 0
                    else base_params.freq_top_step
                )
                new_duration_step = (
                    base_params.duration_step / 2
                    if base_params.duration_grad < 0
                    else base_params.duration_step
                )

            rate = 10000
            new_params = ParamsModel(
                step_number=last_params.step_number + 1,
                label=estimation.label,
                freq_bottom=cls.__limit_value(
                    base_params.freq_bottom + rate * base_params.freq_bottom_grad,
                    max_value=base_params.freq_top - 1,
                ),
                freq_top=cls.__limit_value(
                    base_params.freq_top + rate * base_params.freq_top_grad,
                    min_value=base_params.freq_bottom + 1,
                ),
                duration=cls.__limit_value(
                    base_params.duration + rate * base_params.duration_grad,
                    min_value=10,
                    max_value=975,
                ),
                freq_bottom_step=new_freq_bottom_step,
                freq_top_step=new_freq_top_step,
                duration_step=new_duration_step,
            )
            await OptimizerRepository.create(new_params)
