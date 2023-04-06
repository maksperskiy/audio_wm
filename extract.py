import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq, irfft, fft, ifft, dct, fftfreq

# class prediction
import json
import requests
import zipfile


class Extractor:
    def __init__(self) -> None:
        labels_file = zipfile.ZipFile("./models/classifier/00000001/model.tflite").open(
            "yamnet_label_list.txt"
        )
        self.labels = [l.decode("utf-8").strip() for l in labels_file.readlines()]

        # Число байт
        P = 3
        # Берем файл и разбиваем его на фрагметы длиной N
        self.N = 100000

        # Увеличиваем длину сообщения на 2 (длина CRC)
        self.P = P + 2

        # Смещение - для проверки устойчивости, если фрейм сигнала будет сдвинут
        self.Shift = 0  # 4256

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

    @classmethod
    def predict_class(cls, signal):
        # signal = audio[el:el+15600].tolist()
        result = requests.post(
            "http://localhost:8501/v1/models/classifier:predict",
            data=json.dumps({"instances": signal}),
        )
        if result:
            return cls.labels[
                np.array(json.loads(result.content)["predictions"]).argmax()
            ]

    @classmethod
    def get_class_group(cls, prediction):
        pass

    @classmethod
    def get_class_params(cls, group):
        return 1750, 8500, 20

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
            # prediction = self.predict_class(dt)
            # class_group = self.get_class_group(prediction)
            # bottom_freq, top_freq, duration = self.get_class_params(class_group)
            bottom_freq, top_freq, duration = 1750, 8500, 20

            cnt, crc, mes = self.process_frame(
                dt, samplerate, bottom_freq, top_freq, duration
            )
            count = count + cnt
            success = success + crc
            if message == 0 and crc == 1:
                message = mes
            if message != 0 and crc == 1 and message != mes:
                print("Wrong message!!!")
        if count and success:
            success_ratio = 100 * success / count
        else:
            print("No messages were found")
        return message, success_ratio

    def process(self, filename="injected_out.wav"):
        # Чтение исходного файла
        samplerate, data = wavfile.read(filename)

        if len(data.shape) == 2:
            return (
                self.process_data(data[:, 0], samplerate),
                self.process_data(data[:, 1], samplerate),
            )
        elif len(data.shape) == 1:
            return (self.process_data(data, samplerate),)
        else:
            raise Exception
