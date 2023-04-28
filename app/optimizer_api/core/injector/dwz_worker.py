import numpy as np
from scipy.fft import dct, idct

from .helper import write_info_dct, write_info_dct_cpp
from .parametrs import Alg_parametrs


class DWZ_worker:
    def __init__(self, param: Alg_parametrs):
        self.bottom_freq = param.bottom_freq
        self.top_freq = param.top_freq
        self.duration = param.duration
        self.k = param.k
        self.N = param.N
        self.DWM = param.DWM
        self.count_bit_DWZ = param.count_bit_DWZ

    def process_frame_inject(self, frame, samplerate):
        # write_info_dct_cpp(frame, "test_data_frame_before_inject.txt")
        # Ищем максимум
        pos = (
            np.argmax(frame)
            if abs(frame.max()) > abs(frame.min())
            else np.argmin(frame)
        )
        # Берем интервал = duration мс
        radius = int(self.duration * samplerate / 2000)

        pos_f = int(pos - radius)
        pos_t = int(pos + radius)
        if pos_f < 0 or pos_t > len(frame):
            return frame, 0

        fr = frame[pos_f:pos_t]
        if len(fr) == 0:
            return frame, 0

        # print(f"pos_freq === {pos_f}; frame[pos_f]={frame[pos_f]}; radius={radius}")
        # print(f"pos_top === {pos_t}; frame[pos_t]={frame[pos_t]}")
        # write_info_dct_cpp(fr, "test_real_data_before_dct.txt")
        dfr = dct(fr)
        # write_info_dct_cpp(dfr, "test_real_data_after_dct.txt") # ------------------------------------------

        # Обнуляем частоты
        points_per_freq = 2 * len(dfr) / samplerate
        bfi = int(points_per_freq * self.bottom_freq)
        tfi = int(points_per_freq * self.top_freq)

        interval_len = int((tfi - bfi) / self.count_bit_DWZ)
        mid = int(interval_len / 2)
        dfr[0 : bfi - 1] = 0  # зачем на единички отступаем?
        dfr[tfi + 1 : len(dfr)] = 0

        for j in range(0, self.count_bit_DWZ):
            ind = bfi + interval_len * j
            bit = (self.DWM >> j) & 1

            cp = np.copy(dfr[ind : ind + interval_len])

            # print(f"->bfi={bfi}; interval_index= {j}; ind={ind}")

            max_amplitude = np.max(np.abs(dfr[ind : ind + interval_len]))
            normal_max_left_part = np.max(np.abs(cp[0:mid])) / max_amplitude
            normal_max_right_part = np.max(np.abs(cp[mid:interval_len])) / max_amplitude

            # Первая версия алгоритма
            if bit == 0:
                cp[0:mid] = 0
                cp[mid:interval_len] = cp[mid:interval_len] * normal_max_right_part
            else:
                cp[mid:interval_len] = 0
                cp[0:mid] = cp[0:mid] * normal_max_left_part
            # Проверяем результат встраивания
            m1 = np.max(np.abs(cp[0:mid]))
            m2 = np.max(np.abs(cp[mid:interval_len]))
            bt = 1 if m1 > m2 else 0
            if bit != bt:
                # Встраивание не удалось, возвращаем исходный фрейм
                return frame, 0

            dfr[ind : ind + interval_len] = cp

        res = np.copy(frame)
        res[pos_f:pos_t] = res[pos_f:pos_t] - idct(dfr)
        # write_info_dct_cpp(res, "test_data_frame_after_inject.txt")
        return res, 1

    def process_frame_extract(self, frame, samplerate):
        #    pos = np.argmax(frame)
        pos = (
            np.argmax(frame)
            if abs(frame.max()) > abs(frame.min())
            else np.argmin(frame)
        )
        # Берем интервал = duration мс
        l = int(self.duration * samplerate / 1000)
        # А еще можно попробовать сделать сдвиг... А не середину
        pos_f = int(pos - l / 2)
        pos_t = int(pos + l / 2)
        fr = frame[pos_f:pos_t]
        if len(fr) == 0:
            return 0, 0, 0

        d = dct(fr)

        points_per_freq = 2 * len(d) / samplerate
        # Обнуляем частоты
        bfi = int(points_per_freq * self.bottom_freq)
        tfi = int(points_per_freq * self.top_freq)
        b = int((tfi - bfi) / self.count_bit_DWZ)
        mid = int(b / 2)
        d[0 : bfi - 1] = 0
        d[tfi + 1 : len(d)] = 0

        res = 0
        for j in range(0, self.count_bit_DWZ):
            ind = bfi + b * j
            t1 = d[ind : ind + mid]
            t2 = d[ind + mid : ind + b]
            m1 = np.max(np.abs(t1))
            m2 = np.max(np.abs(t2))
            bit = 1 if m1 < m2 else 0
            res = res | bit << j
            # print(f"{j}) labs_left={m1}; abs_right={m2}; bit={bit}")
        message = res >> 16
        checkX = res >> 8 & 0xFF
        checkO = res & 0xFF
        SX = 0
        for i in range(0, self.count_bit_DWZ - 16):
            SX = SX ^ (message >> i & 1) << (i % 8)
        SO = 0
        for i in range(0, self.count_bit_DWZ - 16):
            SO = SO | (message >> i & 1) << (i % 8)

        s = ""
        for i in range(0, self.count_bit_DWZ):
            s = s + str((res >> i) & 1)
        expected_dvm = ""
        for i in range(0, self.count_bit_DWZ):
            expected_dvm = expected_dvm + str((self.DWM >> i) & 1)
        # print(f"detected dvm = {s}")
        # print(f"expected dvm = {expected_dvm}")

        # print(f"detected res = {hex(res)}")
        return (
            SX == checkX or SO == checkO,
            1 if SX == checkX and SO == checkO else 0,
            message,
        )


# точно ли проверяем хотя бы один проверочный байт?
