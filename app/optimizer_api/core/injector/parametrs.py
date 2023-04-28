class Alg_parametrs:
    def __init__(
        self, DWM=0x123456, bottom_freq=1750, top_freq=8500, duration=20, k=1, N=100000
    ):
        self.DWM = DWM
        self.bottom_freq = bottom_freq
        self.top_freq = top_freq
        self.duration = duration
        self.k = k
        self.N = N
        self.count_bit_DWZ = 0
        self.expand()

    def calculate_count_byte(self):
        temp = self.DWM
        count = 0
        while temp:
            temp = temp // 256
            count += 1
        return count * 8

    def expand(self):
        # Число байт в сообщении
        P = self.calculate_count_byte()
        # Считаем контрольный байт через функцию XOR
        S = 0
        DWM = self.DWM
        for i in range(0, P):
            S = S ^ (DWM >> i & 1) << (i % 8)
        DWM = DWM << 8 | S
        # Считаем второй контрольный байт через функцию OR
        S = 0
        for i in range(0, P):
            S = S | (DWM >> i & 1) << (i % 8)
        self.DWM = DWM << 8 | S
        # Длина сообщения увеличилась на 2 байта
        self.count_bit_DWZ = P + 16

    def get_clear_dwm(self):
        return (self.DWM) >> 16


class Quality_parameters:
    def __init__(self, max_count_dwm: int, inject_count_dwm: int, SNR: float):
        self.max_count_dwm = max_count_dwm
        self.inject_count_dwm = inject_count_dwm
        self.SNR = SNR

    def __str__(self):
        return f"max_count_dwm = {self.max_count_dwm}; inject_count_dwm = {self.inject_count_dwm}; p = {self.inject_count_dwm / self.max_count_dwm}; SNR = {self.SNR};"
