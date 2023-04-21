import json
import os

import librosa
import numpy as np
import pandas as pd
import requests
from scipy.io import wavfile

labels_df = pd.read_csv("./models/classifier/00000002/assets/yamnet_class_map.csv")
labels = {i: label for i, label in enumerate(labels_df["display_name"].tolist())}


def split_wav_files(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for file_name in os.listdir(input_folder_path):
        if file_name.endswith(".wav"):
            file_path = os.path.join(input_folder_path, file_name)
            try:
                rate, save_data = wavfile.read(file_path)

                new_rate = 16000
                data, new_rate = librosa.load(file_path, sr=new_rate)

                rate_ratio = rate / new_rate

                for i in range(0, len(data), 15600):
                    start = i
                    end = i + 15600

                    if len(data[start:end]) < 15600:
                        break

                    if len(data.shape) == 2:
                        signal = data[start:end, 0].tolist()
                    else:
                        signal = data[start:end].tolist()

                    result = requests.post(
                        "http://localhost:8501/v1/models/classifier:predict",
                        data=json.dumps({"inputs": signal}),
                    )

                    if result:
                        try:
                            label = labels[
                                np.array(
                                    json.loads(result.content)["outputs"]["output_0"]
                                ).argmax()
                            ]

                            new_file_name = f"{os.path.splitext(file_name)[0]}_{i/15600}_{label}.wav"

                            new_file_path = os.path.join(
                                output_folder_path, new_file_name
                            )
                            wavfile.write(
                                new_file_path,
                                rate,
                                save_data[
                                    int(start * rate_ratio) : int(end * rate_ratio)
                                ],
                            )
                        except:
                            pass
            except:
                pass


if __name__ == "__main__":
    split_wav_files("./data/fold1/", "./data/fold2/")
