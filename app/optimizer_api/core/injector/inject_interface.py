import os
import random
import string
import subprocess
from typing import List

from .parametrs import Alg_parametrs
from .wrapper_injector_detector import read_data_from_file, write_data_in_file


def inject_in_stream(streams: List[List], samplerate: int, param: Alg_parametrs):
    sign = "".join(random.choice(string.ascii_lowercase) for _ in range(9))
    input_file_name = f"./stream123456_temp_test_data_{sign}"
    output_file_name = f"./injected123456_temp_test_data_{sign}"
    write_data_in_file(input_file_name, streams, samplerate, param)

    print(f"start subprocess")
    # path_to_app = '/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/bin/Debug/video_test'
    # path_to_app = '/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/bin/Release/video_test'
    path_to_app = "/home/INTEXSOFT/maksim.stupakevich/work/audio_cls/injector/C_code/bin/Release/video_test"  # locally
    path_to_app = "/app/optimizer_api/core/injector/C_code/bin/Release/video_test"  # in docker
    result = subprocess.run(
        [path_to_app, "-i", input_file_name, output_file_name], stdout=subprocess.PIPE
    )
    print(f" subprocess stdout")
    print(result.stdout.decode("utf-8"))
    print(f"end subprocess")

    data = read_data_from_file(output_file_name)
    # delete files
    try:
        os.remove(input_file_name)
        os.remove(output_file_name)
    except:
        pass

    return data
