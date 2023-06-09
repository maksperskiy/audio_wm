import numpy as np

from app.optimizer_api.core.injector.inject_interface import inject_in_stream
from app.optimizer_api.core.injector.parametrs import Alg_parametrs
from app.optimizer_api.database.audio_provider import FileProvider
from app.optimizer_api.database.models import ParamsHistoryModel
from app.optimizer_api.database.repositories import OptimizerRepository
from app.optimizer_api.schemas.requests.audio import EstimationRequest
from app.optimizer_api.schemas.responses.audio import LabelsResponse, SoundResponse

import math


class AudioHandler:
    @staticmethod
    async def get_labels():
        return LabelsResponse(labels=FileProvider.labels)

    @staticmethod
    async def process_sound(sound, samplerate, params):
        result = inject_in_stream(sound.T, samplerate, params)
        
        if len(sound.shape) == 2:
            injected_sound = np.column_stack(
                [
                    np.array(result[0][0], dtype=np.int16),
                    np.array(result[1][0], dtype=np.int16),
                ]
            )
            sound_noise_ratio = (result[0][1].SNR + result[1][1].SNR) / 2
            success_ratio = (
                result[0][1].inject_count_dwm / result[0][1].max_count_dwm
                + result[1][1].inject_count_dwm / result[1][1].max_count_dwm
            ) / 2
        else:
            injected_sound = np.array(result[0][0], dtype=np.int16)
            sound_noise_ratio = result[0][1].SNR
            success_ratio = result[0][1].inject_count_dwm / result[0][1].max_count_dwm

        return injected_sound, sound_noise_ratio if not math.isinf(sound_noise_ratio) else 0, success_ratio

    @classmethod
    async def get_audio(cls, label: str):
        sound, samplerate = await FileProvider.get_random_audio(label)
        params = await OptimizerRepository.get_last_params(label)

        if not params:
            params = await OptimizerRepository.intialize_params(label=label)

        if sound.dtype == "int32":
            sound = (sound >> 16).astype(np.int16)
        message = 0x123456

        params = Alg_parametrs(
            N=10000,
            DWM=message,
            bottom_freq=params.freq_bottom,
            top_freq=params.freq_top,
            duration=params.duration,
        )

        injected_sound, sound_noise_ratio, success_ratio = await cls.process_sound(sound, samplerate, params)

        result = SoundResponse(
            label=label,
            message=message,
            extracted_message=message if success_ratio else 0,
            sound_array=sound.tolist(),
            injected_sound_array=injected_sound.tolist(),
            samplerate=samplerate,
            sound_noise_ratio=sound_noise_ratio,
            success_ratio=success_ratio,
        )
        return result

    @staticmethod
    def __limit_value(value, min_value=0, max_value=20000):
        if value > max_value:
            return max_value
        elif value < min_value:
            return min_value
        return int(value)

    @staticmethod
    def __count_reward(expert_score, sound_noise_ratio, success_ratio):
        expert_score_part = expert_score / 5
        sound_noise_ratio_part = 1 / sound_noise_ratio if sound_noise_ratio else 0
        success_ratio_part = success_ratio
        return expert_score_part * sound_noise_ratio_part * success_ratio_part

    @classmethod
    async def optimize(
        cls,
        estimation: EstimationRequest,
        batch_size: int = 1,
    ) -> None:
        last_params = await OptimizerRepository.get_last_params(estimation.label)
        base_params = await OptimizerRepository.get_last_base_params(estimation.label)

        if (
            base_params.expert_score != None
            and base_params.sound_noise_ratio != None
            and base_params.success_ratio != None
        ):
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
                "label": base_params.label,
                "step_number": base_params.step_number,
                "experiment_number": base_params.experiment_number,
            }
            updates = {
                "expert_score": estimation.expert_score,
                "sound_noise_ratio": estimation.sound_noise_ratio,
                "success_ratio": estimation.success_ratio,
                "current_param": 0,
                "batch_size": batch_size,
            }
            await OptimizerRepository.update(updates, **params)

            new_params = ParamsHistoryModel(
                step_number=last_params.step_number + 1,
                label=estimation.label,
                experiment_number=last_params.experiment_number,
                param_number=0,
                freq_bottom=cls.__limit_value(
                    base_params.freq_bottom + base_params.freq_bottom_step,
                    max_value=base_params.freq_top - 500,
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
            gradient = reward - float(base_reward)
            params = {
                "label": base_params.label,
                "step_number": base_params.step_number,
                "experiment_number": base_params.experiment_number,
            }
            updates = {
                "freq_bottom_grad": float(base_params.freq_bottom_grad) + gradient
                if base_params.freq_bottom_grad
                else gradient,
                "current_param": base_params.current_param + 1,
            }
            await OptimizerRepository.update(updates, **params)

            if base_params.current_param // base_params.batch_size == 1:
                new_params = ParamsHistoryModel(
                    step_number=last_params.step_number + 1,
                    label=estimation.label,
                    experiment_number=last_params.experiment_number,
                    param_number=1,
                    freq_bottom=base_params.freq_bottom,
                    freq_top=cls.__limit_value(
                        base_params.freq_top + base_params.freq_top_step,
                        min_value=base_params.freq_bottom + 500,
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
            gradient = reward - float(base_reward)
            params = {
                "label": base_params.label,
                "step_number": base_params.step_number,
                "experiment_number": base_params.experiment_number,
            }
            updates = {
                "freq_top_grad": float(base_params.freq_top_grad) + gradient
                if base_params.freq_top_grad
                else gradient,
                "current_param": base_params.current_param + 1,
            }
            await OptimizerRepository.update(updates, **params)

            if base_params.current_param // base_params.batch_size == 2:
                new_params = ParamsHistoryModel(
                    step_number=last_params.step_number + 1,
                    label=estimation.label,
                    experiment_number=last_params.experiment_number,
                    param_number=2,
                    freq_bottom=base_params.freq_bottom,
                    freq_top=base_params.freq_top,
                    duration=cls.__limit_value(
                        base_params.duration + base_params.duration_step,
                        min_value=20,
                        max_value=975,
                    ),
                    freq_bottom_step=base_params.freq_bottom_step,
                    freq_top_step=base_params.freq_top_step,
                    duration_step=base_params.duration_step,
                )
                await OptimizerRepository.create(new_params)

        elif last_params.param_number == 2:
            # set to base duration grad
            gradient = reward - float(base_reward)
            params = {
                "label": base_params.label,
                "step_number": base_params.step_number,
                "experiment_number": base_params.experiment_number,
            }
            updates = {
                "duration_grad": float(base_params.duration_grad) + gradient
                if base_params.duration_grad
                else gradient,
                "current_param": base_params.current_param + 1,
            }
            await OptimizerRepository.update(updates, **params)
            # create new base with updated params, steps, empty param_number, reward and grads
            # reset steps if step_number more that xx

            if base_params.current_param // base_params.batch_size == 3:
                if (
                    base_params.freq_bottom_step <= 1
                    and base_params.freq_top_step <= 1
                    and base_params.duration_step <= 1
                ):
                    new_freq_bottom_step = 100
                    new_freq_top_step = 100
                    new_duration_step = 100
                else:
                    new_freq_bottom_step = (
                        base_params.freq_bottom_step / 2
                        if base_params.freq_bottom_grad <= 0
                        else base_params.freq_bottom_step
                    )
                    new_freq_top_step = (
                        base_params.freq_top_step / 2
                        if base_params.freq_top_grad <= 0
                        else base_params.freq_top_step
                    )
                    new_duration_step = (
                        base_params.duration_step / 2
                        if base_params.duration_grad <= 0
                        else base_params.duration_step
                    )

                if last_params.step_number // 84 >= 1 or (
                    base_params.freq_bottom_step <= 1
                    and base_params.freq_top_step <= 1
                    and base_params.duration_step <= 1
                ):
                    rate = 1000
                else:
                    rate = 10000

                new_params = ParamsHistoryModel(
                    step_number=last_params.step_number + 1,
                    label=estimation.label,
                    experiment_number=last_params.experiment_number,
                    freq_bottom=cls.__limit_value(
                        base_params.freq_bottom
                        + rate
                        * (base_params.freq_bottom_grad / base_params.batch_size),
                        max_value=base_params.freq_top - 500,
                    ),
                    freq_top=cls.__limit_value(
                        base_params.freq_top
                        + rate * (base_params.freq_top_grad / base_params.batch_size),
                        min_value=base_params.freq_bottom + 500,
                    ),
                    duration=cls.__limit_value(
                        base_params.duration
                        + rate * (base_params.duration_grad / base_params.batch_size),
                        min_value=20,
                        max_value=975,
                    ),
                    freq_bottom_step=new_freq_bottom_step,
                    freq_top_step=new_freq_top_step,
                    duration_step=new_duration_step,
                )
                await OptimizerRepository.create(new_params)

    @staticmethod
    async def reset_label(label: str) -> None:
        last_params = await OptimizerRepository.get_last_params(label)
        if last_params:
            await OptimizerRepository.intialize_params(
                label=label, experiment_number=last_params.experiment_number + 1
            )
