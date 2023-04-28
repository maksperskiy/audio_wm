import math

import numpy as np
from scipy.io import wavfile

from dwz_worker import DWZ_worker
from parametrs import Alg_parametrs


def process_data_new(data, samplerate, worker_dvz: DWZ_worker):
    res = []
    count = 0
    count_fragment_for_inject_dwz = math.ceil(len(data) / worker_dvz.N)
    for i in range(0, count_fragment_for_inject_dwz):
        fragment_start = int(i * worker_dvz.N)
        fragment_end = min(int((i + 1) * worker_dvz.N), len(data))
        dt = np.copy(data[fragment_start:fragment_end])

        # print(f"{i}) fragment_start={fragment_start}; fragment_end={fragment_end}")

        frame, count_dwz_injected = worker_dvz.process_frame_inject(dt, samplerate)
        res = np.concatenate([res, frame])
        count = count + count_dwz_injected
    return res, count


def process_data(data, samplerate, worker_dvz: DWZ_worker):
    return process_data_new(data, samplerate, worker_dvz)


def test_inject(file_path: str, file_out_path: str, param: Alg_parametrs):
    worker_dvz = DWZ_worker(param)
    samplerate, data = wavfile.read(file_path)

    print(f"samplerate={samplerate}")

    # Обработка данных каждого канала
    left, lcnt = process_data(data[:, 0], samplerate, worker_dvz)
    right, rcnt = process_data(data[:, 1], samplerate, worker_dvz)

    print(f"Count = {lcnt+rcnt}")
    max_count_old = int(2 * len(data) / worker_dvz.N)
    max_count_new = 2 * math.ceil(len(data) / worker_dvz.N)
    print(f"Max count = {max_count_new}")
    print(f"Quality = {(lcnt+rcnt)/max_count_new}")

    # Сборка и нормализация результирующего сигнала
    marked_signal = np.column_stack((left, right))
    normalized_signal = np.int16((marked_signal / marked_signal.max()) * 32767)

    print(f"marked_signal:{marked_signal};")
    print(f"marked_signal.max():{marked_signal.max()};")
    print(f"max(left):{max(left)}; max(right):{max(right)}")
    # Запись результирующего файла
    wavfile.write(file_out_path, samplerate, normalized_signal)
    print(f"end writed file")
    return data, marked_signal


# dcgjvjufntkmyfz aeyrwbz lkz ghjdthrb rjhhtrnyjcnb gk.cjdjuj rjlf
def test_inject_for_c_check(data, samplerate: int, param: Alg_parametrs):
    worker_dvz = DWZ_worker(param)

    # Обработка данных каждого канала
    left, lcnt = process_data(data[:, 0], samplerate, worker_dvz)
    right, rcnt = process_data(data[:, 1], samplerate, worker_dvz)

    print(f"Count = {lcnt+rcnt}")
    max_count_old = int(2 * len(data) / worker_dvz.N)
    max_count_new = 2 * math.ceil(len(data) / worker_dvz.N)
    print(f"Max count = {max_count_new}")
    print(f"Quality = {(lcnt+rcnt)/max_count_new}")

    print(f"end writed file")
    return left, right


def test_inject_in_file(file_path, file_out_path, param: Alg_parametrs):
    # Чтение исходного файла

    data, marked_signal = test_inject(file_path, file_out_path, param)

    # Вычисляем шум
    noise = data[0 : len(marked_signal)] - marked_signal

    # Вычисляем соотношение сигнал/шум
    # Вычисляем среднеквадратичные амплитуды сигнала и шума
    # Делим на M, так как без этого происходит переполнение
    M = np.max(data)
    A = math.sqrt(((data / M) ** 2).sum())
    N = math.sqrt(((noise / M) ** 2).sum())

    # Вычисляем соотношение сигнал/шум
    SNR = 10 * np.log10((A / N) ** 2)

    #    print(f"noise:{noise}")

    # plt.plot(noise[240000:280000])
    # plt.show()

    print(f"SNR = {SNR}")


def create_test_inject_data(file_path: str, file_out_path: str, param: Alg_parametrs):
    worker_dvz = DWZ_worker(param)
    samplerate, data = wavfile.read(file_path)

    print(f"samplerate={samplerate}")

    # Обработка данных каждого канала
    left, lcnt = process_data(data[:, 0], samplerate, worker_dvz)
    right, rcnt = process_data(data[:, 1], samplerate, worker_dvz)

    print(f"Count = {lcnt+rcnt}")
    max_count_old = int(2 * len(data) / worker_dvz.N)
    max_count_new = 2 * math.ceil(len(data) / worker_dvz.N)
    print(f"Max count = {max_count_new}")
    print(f"Quality = {(lcnt+rcnt)/max_count_new}")

    # Сборка и нормализация результирующего сигнала
    marked_signal = np.column_stack((left, right))
    normalized_signal = np.int16((marked_signal / marked_signal.max()) * 32767)

    # Запись результирующего файла
    wavfile.write(file_out_path, samplerate, normalized_signal)
    print(f"end writed file")
    return data, marked_signal
