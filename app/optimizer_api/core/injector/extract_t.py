import math

import numpy as np
from scipy.io import wavfile

from dwz_worker import DWZ_worker
from parametrs import Alg_parametrs

# Смещение - для проверки устойчивости, если фрейм сигнала будет сдвинут
Shift = 0  # 4256


def process_data_new(data, samplerate, worker_dvz: DWZ_worker):
    count = 0
    success = 0
    message = 0
    count_fragment_for_inject_dwz = math.ceil(len(data) / worker_dvz.N)
    for i in range(0, count_fragment_for_inject_dwz):
        fragment_start = int(i * worker_dvz.N) + Shift
        fragment_end = min(int((i + 1) * worker_dvz.N) + Shift, len(data))
        dt = np.copy(data[fragment_start:fragment_end])
        cnt, crc, mes = worker_dvz.process_frame_extract(dt, samplerate)
        count = count + cnt
        success = success + crc
        if crc == 1:
            if message == 0:
                message = mes
            if message != 0 and message != mes:
                print("Wrong message!!!")
    if count == 0:
        print(f"res={0}")
    else:
        print(f"res={100*success/count}")


def process_data(data, samplerate, worker_dvz: DWZ_worker):
    return process_data_new(data, samplerate, worker_dvz)


def test_extract_from_file(file_path, param: Alg_parametrs):
    worker_dvz = DWZ_worker(param)
    # Чтение исходного файла
    samplerate, data = wavfile.read(file_path)

    extract_1 = process_data(data[:, 0], samplerate, worker_dvz)
    extract_2 = process_data(data[:, 1], samplerate, worker_dvz)
    # print(hex(extract_1))
    # print(hex(extract_2))
