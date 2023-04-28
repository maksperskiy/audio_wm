from typing import List

from .parametrs import Alg_parametrs, Quality_parameters


def read_data_from_file(file_name: str):
    res = []
    with open(file_name, "r") as file:
        count_stream = int(file.readline())
        for i in range(0, count_stream):
            max_count_dwm = float(file.readline())
            inject_count_dwm = float(file.readline())
            SNR = float(file.readline())
            data = file.readline()
            result = [float(x) for x in data.split()]
            # print(f"{result}")
            res.append(
                (
                    result,
                    Quality_parameters(
                        max_count_dwm=max_count_dwm,
                        inject_count_dwm=inject_count_dwm,
                        SNR=SNR,
                    ),
                )
            )
    return res


def write_data_in_file(
    file_name: str, data: List[List], samplerate: int, parametrs: Alg_parametrs
):
    with open(file_name, "w") as file:
        file.write(str(len(data)) + "\n")
        for stream in data:
            file.write(str(len(stream)) + "\n")
            for i in stream:
                file.write(str(i) + " ")
        file.write(str(samplerate) + "\n")
        file.write(str(parametrs.duration) + "\n")
        file.write(str(parametrs.bottom_freq) + "\n")
        file.write(str(parametrs.top_freq) + "\n")
        file.write(str(parametrs.get_clear_dwm()) + "\n")
        file.write(str(parametrs.N) + "\n")
