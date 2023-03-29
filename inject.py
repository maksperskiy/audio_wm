import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq, irfft, fft, ifft, dct, fftfreq, idct

# Встраиваемое сообщение
DWM = 0x123456  # 0001 0010 0011 0100 0101 0110
# Число байт в сообщении
P = 3
# Считаем контрольный байт через функцию XOR
S = 0
for i in range(0, 8*P):
    S = S ^ (DWM >> i & 1) << (i % 8)
DWM = DWM << 8 | S
# Считаем второй контрольный байт через функцию OR
S = 0
for i in range(0, 8*P):
    S = S | (DWM >> i & 1) << (i % 8)
DWM = DWM << 8 | S
# Длина сообщения увеличилась на 2 байта
P = P + 2

# Берем файл и разбиваем его на фрагметы длиной N
N = 100000
# В каждом фрагменте делаем Дискретное косинусовое преобразование
# В результате преобразования фильтруем частоты, которые задаем в настройках - т.е. наиболее значимые частоты
# Оставшийся частотный диапазон делим на m частей, где m = размер диапазона / длину сообщения в битах
# Каждую часть делим на 2 подчасти
# Если бит = 0 - зануляем первую половину
# Если = 1 - зануляем вторую половину
# "зануляем" - нормируем сигнал так, чтобы максимальная амплитуда была равна минимальной
# Восстанавливаем idct для полученного нового сигнала - это шум
# Далее из основного сигнала вычитаем данный шум
bottom_freq = 1750
top_freq = 8500
duration = 20
k = 1

# Обработка фрейма i
def process_frame(frame, samplerate):
    # Ищем максимум
    pos = np.argmax(frame) if abs(frame.max()) > abs(frame.min()) else np.argmin(frame)
    # Берем интервал = duration мс
    l = int(duration * samplerate / 1000)
    pos_f = int(pos - l / 2)
    pos_t = int(pos + l / 2)
    fr = frame[pos_f: pos_t]
    if (len(fr) == 0):
        return frame, 0
    
    dfr = dct(fr)
    # Обнуляем частоты
    points_per_freq = 2 * len(dfr) / samplerate
    bfi = int(points_per_freq * bottom_freq)
    tfi = int(points_per_freq * top_freq)
    b = int((tfi-bfi) / (P*8))
    dfr[0:bfi-1] = 0
    dfr[tfi+1:len(dfr)] = 0

    for j in range(0, P * 8):
        ind = bfi+b*j
        bit = (DWM >> j) & 1
        mid = int(b/2)
        cp = np.copy(dfr[ind:ind+b])

        # Первая версия алгоритма
        if bit == 0:
            ddd = dfr[ind:ind+mid]
            cp[0:mid] = 0
            cp[mid:b] = cp[mid:b] * np.max(np.abs(cp[mid:b])) / np.max(np.abs(dfr[ind:ind+b]))
        else:
            ddd = dfr[ind+mid:ind+b]
            cp[mid:b] = 0
            cp[0:mid] = cp[0:mid] * np.max(np.abs(cp[0:mid])) / np.max(np.abs(dfr[ind:ind+b]))
        # Проверяем результат встраивания
        m1 = np.max(np.abs(cp[0:mid]))
        m2 = np.max(np.abs(cp[mid:b]))
        bt = 1 if m1 > m2 else 0
        if bit != bt:
            # Встраивание не удалось, возвращаем исходный фрейм
            return frame, 0

        # Вторая версия алгоритма - показала хуже результат
#        mx = np.max(cp)
#        mn = np.min(cp)
#        av = np.average(cp)
        # Проверяем на соответствие биту, который нужно закодировать
#        check = 1 if (2 * av - mn - mx) > 0 else 0
        # Если не соответствует, корректируем
#        if check != bit:
            # Величина сдвига и направление сдвига
#            delta = (2 * bit - 1) * (1 + k) * b * abs((mx + mn) / 2 - av) / (b - 2)
            # Сдвигаем частоты
#            cp = cp + delta * (1 - (np.int16((mx-cp) / abs(mx-mn) / 1) + np.int16((cp-mn) / abs(mx-mn) / 1)))

        # Повторно проверяем на соответствие биту, который нужно закодировать
#        mx = np.max(cp)
#        mn = np.min(cp)
#        av = np.average(cp)
#        check = 1 if (2 * av - mn - mx) > 0 else 0

        # Если снова не соответствует, ошибка вставки
#        if check != bit:
            # Возвращаем исходный фрейм с признаком неуспеха
#            return frame, 0
        
        dfr[ind:ind+b] = cp

    res = np.copy(frame)
    res[pos_f: pos_t] = res[pos_f: pos_t] - idct(dfr)
    return res, 1

def process_data(data, samplerate):
    res = []
    count = 0
    for i in range(0, int(len(data) / N + 1)):
        fr = int(i*N)
        to = min(int((i+1)*N), len(data))
        dt = np.copy(data[fr:to])
        frame, cnt = process_frame(dt, samplerate)
        res = np.concatenate([res, frame])
        count = count + cnt
    return res, count

    
# Чтение исходного файла
samplerate, data = wavfile.read('/Users/sibirexe/Desktop/Digital Watermark/Files/Source/Futbolnyj_match.wav')

print(samplerate)

# Обработка данных каждого канала
left, lcnt = process_data(data[:,0], samplerate)
right, rcnt = process_data(data[:,1], samplerate)

print(f"Count = {lcnt+rcnt}")
print(f"Max count = {int(2*len(data)/N)}")
print(f"Quality = {(lcnt+rcnt)/int(2*len(data)/N)}")

# Сборка и нормализация результирующего сигнала
marked_signal = np.column_stack((left, right))
normalized_signal = np.int16((marked_signal / marked_signal.max()) * 32767)

# Запись результирующего файла
wavfile.write('/Users/sibirexe/Desktop/Digital Watermark/Files/Res/Futbolnyj_match.wav', samplerate, normalized_signal)

# Вычисляем шум
noise = data[0:len(marked_signal)] - marked_signal

# Вычисляем соотношение сигнал/шум

# Вычисляем среднеквадратичные амплитуды сигнала и шума
# Делим на M, так как без этого происходит переполнение
M = np.max(data)
A = math.sqrt(((data/M) ** 2).sum())
N = math.sqrt(((noise/M) ** 2).sum())

# Вычисляем соотношение сигнал/шум
SNR = 10 * np.log10((A / N) ** 2)

plt.plot(noise[890500:892000])
plt.show()

print(f"SNR = {SNR}")

# Варианты доработки
# 1. Контрольные суммы байтов или полубайтов
# 2. Проверка встраивания сигнала, и отмена, если не удалось
# 3. Разбиение частотного диапазона на 4 части, и зануление того фрагмента, где ниже максимум