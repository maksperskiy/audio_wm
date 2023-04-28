import math
import random
import time

import numpy as np
from scipy.io import wavfile

from dwz_worker import DWZ_worker
from extract_t import test_extract_from_file
from helper import get_data_from_file
from inject_interface import inject_in_stream
from inject_t import test_inject_for_c_check, test_inject_in_file
from parametrs import Alg_parametrs
from wrapper_injector_detector import read_data_from_file, write_data_in_file


def test_1():
    file_path = (
        "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/out.wav"
    )
    # file_path = "/home/INTEXSOFT/alexander.polianski/Downloads/test2.wav"

    param = Alg_parametrs()
    file_out_path = f"{file_path}_res"
    test_inject_in_file(file_path, file_out_path, param)

    print(f" inject finished  *****    ")
    test_extract_from_file(file_out_path, param)

    print(f" extract finished  *****    ")


def test_2():
    data = get_data_from_file(
        "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/test_data/test_data_frame_before_inject.txt"
    )
    param = Alg_parametrs()
    worker_dvz = DWZ_worker(param)
    samplerate = 44100
    print(f"len(data)={len(data)}")
    # for index in range(0, len(data)):
    for index in range(0, 1):
        if len(data[index]) == 0:
            continue
        res, count_dwz_injected = worker_dvz.process_frame_inject(
            np.asarray(data[index]), samplerate
        )
        print(f"res={res}")


def test_3():
    data = get_data_from_file(
        "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/test_data/test_data_frame_before_inject.txt"
    )
    param = Alg_parametrs()
    worker_dvz = DWZ_worker(param)
    samplerate = 44100
    print(f"len(data)={len(data)}")
    for index in range(0, len(data)):
        if len(data[index]) == 0:
            continue
        start = time.time_ns()
        res, count_dwz_injected = worker_dvz.process_frame_inject(
            np.asarray(data[index]), samplerate
        )
        res_, count_dwz_injected, tt = worker_dvz.process_frame_extract(
            np.asarray(res), samplerate
        )
        end = time.time_ns()
        print(f"time->{(end - start) / 1000} micro sec")
        print(f"***")


def test_4():
    data = get_data_from_file(
        "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/test_data/test_data_frame_after_inject.txt"
    )
    param = Alg_parametrs()
    worker_dvz = DWZ_worker(param)
    samplerate = 44100
    print(f"len(data)={len(data)}")
    data_res = []
    for index in range(0, len(data)):
        if len(data[index]) == 0:
            continue
        print(f"index = {index}")
        res_, count_dwz_injected, tt = worker_dvz.process_frame_extract(
            np.asarray(data[index]), samplerate
        )
        if count_dwz_injected == 1:
            print(f"{index}) True")
            data_res.append(True)
        else:
            print(f"{index}) False")
            data_res.append(False)

        for i in range(0, len(data_res)):
            print(f"{i}) {data_res[i]}")
        print(f"***")


def test_python_extract():
    file_path = "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/out.wav_123_res.wav"
    # file_path = "/home/INTEXSOFT/alexander.polianski/Downloads/test2.wav"

    param = Alg_parametrs()
    test_extract_from_file(file_path, param)

    print(f" extract finished  *****    ")


def test_work_with_file(file_name: str):
    param = Alg_parametrs()
    samplerate, data = wavfile.read(file_name)
    p_data = []
    for i in range(0, len(data[0])):
        p_data.append(data[:, i])
        print(f"{i}) -> {data[:,i]}")

    # left, right = test_inject_for_c_check(data, samplerate, param)

    injectd_sreams_res = inject_in_stream(p_data, samplerate, param)

    print(f"injectd_sreams_res[0][1] = {injectd_sreams_res[0][1]}")
    print(f"injectd_sreams_res[1][1] = {injectd_sreams_res[1][1]}")
    # print(f"res_len = {len(injectd_sreams_res[0][0])};  {len(injectd_sreams_res[1][0])}")
    # print(f"len(left) = {len(left)};  len(right)={len(right)}")

    # Сборка и нормализация результирующего сигнала
    marked_signal = np.column_stack(
        (injectd_sreams_res[0][0], injectd_sreams_res[1][0])
    )
    # marked_signal = np.column_stack((left, right))
    normalized_signal = np.int16((marked_signal / marked_signal.max()) * 32767)

    # Запись результирующего файла
    wavfile.write(f"{file_name}_123_res.wav", samplerate, normalized_signal)
    print(f"end writed file\n")


def check_SNR_opt():
    data = [random.randint(0, 100) for i in range(0, 100000)]
    # Вычисляем шум
    noise = [0 for i in range(0, 100000)]

    # Вычисляем соотношение сигнал/шум

    # Вычисляем среднеквадратичные амплитуды сигнала и шума
    # Делим на M, так как без этого происходит переполнение
    M = np.max(data)
    A = math.sqrt(((data / M) ** 2).sum())
    N = math.sqrt(((noise / M) ** 2).sum())

    N = N + 0.000000001

    # Вычисляем соотношение сигнал/шум
    SNR = 10 * np.log10((A / N) ** 2)
    return SNR


if __name__ == "__main__":
    # test_1()
    file_path = (
        "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/out.wav"
    )

    test_work_with_file(file_path)
    test_python_extract()

    # print(f"optimal SNR = {check_SNR_opt()};")
