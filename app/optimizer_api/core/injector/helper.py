import pickle

import numpy

file_name = "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/myfile1.bin"


def test_binary():
    file = open(file_name, "wb")

    # bt = 0xffad584ed
    bt = 0xFF

    pickle.dump(bt, file)
    file.close()

    test = open(file_name, "rb")
    res = pickle.load(test)
    print(f"res={hex(res)}")


def write_info_dct(data):
    print(f"data = {data.shape}")
    if 4 == 4:
        with open(file_name, "a") as file:
            for i in data:
                file.write(f"{str(i)} ")
            # numpy.save(file, data)
            # file.write(data)
            file.write("\n******\n")


def write_info_dct_cpp(data, file_name):
    with open(file_name, "a") as file:
        file.write(f"{data.shape[0]} ")
        for i in data:
            file.write(f"{str(i)} ")
            # numpy.save(file, data)
            # file.write(data)


def get_data_from_file(file_name: str):
    with open(file_name, "r") as file:
        data = file.read()
    r = [float(x) for x in data.split()]
    result = []
    index = 0
    while index < len(r):
        count = int(r[index])
        index = index + 1
        temp = r[index : index + count]
        if count == 0:
            count = count + 1
        index = index + count - 1
        result.append(temp)

    return result
