import numpy as np
from scipy.fft import rfft, rfftfreq, irfft, fft, ifft, dct, fftfreq


class Extractor:
    def __init__(self, bottom_freq=1750, top_freq=8500, duration=20) -> None:
        # Число байт
        P = 3
        # Берем файл и разбиваем его на фрагметы длиной N
        self.N = 100000

        # Увеличиваем длину сообщения на 2 (длина CRC)
        self.P = P + 2

        # Смещение - для проверки устойчивости, если фрейм сигнала будет сдвинут
        self.Shift = 0  # 4256

        self.bottom_freq = bottom_freq
        self.top_freq = top_freq
        self.duration = duration

    def process_frame(
        self, frame, samplerate, bottom_freq=1750, top_freq=8500, duration=20
    ):
        #    pos = np.argmax(frame)
        pos = np.argmax(np.abs(frame))
        # Берем интервал = duration мс
        l = duration * samplerate // 1000
        # А еще можно попробовать сделать сдвиг... А не середину
        pos_f = int(pos - l / 2)
        pos_t = int(pos + l / 2)
        fr = frame[pos_f:pos_t]
        if len(fr) == 0:
            return 0, 0, 0

        d = dct(fr)

        points_per_freq = 2 * len(d) / samplerate
        # Обнуляем частоты
        bfi = int(points_per_freq * bottom_freq)
        tfi = int(points_per_freq * top_freq)
        b = int((tfi - bfi) / (self.P * 8))
        mid = int(b / 2)
        d[0 : bfi - 1] = 0
        d[tfi + 1 : len(d)] = 0

        res = 0
        for j in range(0, self.P * 8):
            ind = bfi + b * j
            t1 = d[ind : ind + mid]
            t2 = d[ind + mid : ind + b]
            m1 = np.max(np.abs(t1))
            m2 = np.max(np.abs(t2))
            bit = 1 if m1 < m2 else 0
            res = res | bit << j
        message = res >> 16
        checkX = res >> 8 & 0xFF
        checkO = res & 0xFF
        SX = 0
        for i in range(0, 8 * (self.P - 2)):
            SX = SX ^ (message >> i & 1) << (i % 8)
        SO = 0
        for i in range(0, 8 * (self.P - 2)):
            SO = SO | (message >> i & 1) << (i % 8)
        return (
            SX == checkX or SO == checkO,
            1 if SX == checkX and SO == checkO else 0,
            message,
        )

    def process_data(self, data, samplerate):
        count = 0
        success = 0
        res = []
        message = 0
        success_ratio = 0
        for i in range(0, int(len(data) / self.N + 1)):
            fr = int(i * self.N) + self.Shift
            to = min(int((i + 1) * self.N) + self.Shift, len(data))
            dt = np.copy(data[fr:to])

            # params

            cnt, crc, mes = self.process_frame(
                dt, samplerate, self.bottom_freq, self.top_freq, self.duration
            )
            count = count + cnt
            success = success + crc
            if message == 0 and crc == 1:
                message = mes
            if message != 0 and crc == 1 and message != mes:
                print("Wrong message!!!")
        if count and success:
            success_ratio = 100 * success / count
        return message, success_ratio

    def process(self, data, samplerate):
        if len(data.shape) == 2:
            left = self.process_data(data[:, 0], samplerate)
            right = self.process_data(data[:, 1], samplerate)
            return (left[0] or right[0], (left[1]+right[1])/2)
        elif len(data.shape) == 1:
            return self.process_data(data, samplerate)
        else:
            raise Exception
