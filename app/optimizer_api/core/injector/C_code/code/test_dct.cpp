#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <cmath>
#include <chrono>

#include "dct_function.h"
#include "scripts.h"

bool check_double_equals(double a, double b)
{
    constexpr double EPSILON = 0.0001;
    // std::cout<<"fabs(a - b)="<<fabs(a - b)<<"; EPSILON="<<EPSILON<<std::endl;
    return fabs(a - b) < EPSILON;
}

std::vector<std::vector<double>> read_all_data(std::string file_name)
{
    std::ifstream input(file_name);
    std::vector<std::vector<double>> res;
    std::vector<double> temp;
    int counter = 0;
    double numb = 0.0;
    while (input >> counter)
    {
        temp.clear();
        for (int i = 0; i < counter; i++)
        {
            input >> numb;
            temp.push_back(numb);
        }
        res.push_back(temp);
    }
    return res;
}

bool test_equals_data(const std::vector<std::vector<double>> &data_a, const std::vector<std::vector<double>> &data_b)
{
    bool global_result = true;
    bool local_result = true;
    int size = data_a.size();
    if (data_b.size() != size)
    {
        return false;
    }
    for (int i = 0; i < size; i++)
    {
        int temp_size = data_a[i].size();
        if (data_b[i].size() != temp_size)
        {
            return false;
        }
        local_result = true;
        for (int j = 0; j < temp_size; j++)
        {
            if (!check_double_equals(data_a[i][j], data_b[i][j]))
            {
                std::cout << i << ", " << j << ") a=" << data_a[i][j] << "; b=" << data_b[i][j] << ';' << std::endl;
                local_result = false;
                global_result = false;
            }
        }

        std::cout << i << ") result=";
        if (local_result)
        {
            std::cout << " true" << std::endl;
        }
        else
        {
            std::cout << " false" << std::endl;
        }
    }

    return global_result;
}

void test_dct_function()
{
    std::string test_real_data_before_dct = "test_real_data_before_dct.txt";
    std::string test_real_data_after_dct = "test_real_data_after_dct.txt";
    auto data_before_dct = read_all_data(test_real_data_before_dct);
    auto data_after_dct = read_all_data(test_real_data_after_dct);

    std::vector<std::vector<double>> data_res;
    for (auto chunk : data_before_dct)
    {
        data_res.push_back(dct(chunk));
    }

    bool is_data_eqal = test_equals_data(data_after_dct, data_res);
    std::cout << "is_data_eqal = " << is_data_eqal << std::endl;
}

void test_inject_function()
{

    std::string test_real_data_before_dct = "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/test_data/test_data_frame_before_inject.txt";
    std::string test_real_data_after_dct = "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/test_data/test_data_frame_after_inject.txt";
    auto data_before_inject_temp = read_all_data(test_real_data_before_dct);
    auto data_after_inject_temp = read_all_data(test_real_data_after_dct);

    std::vector<std::vector<double>> data_before_inject;
    std::vector<std::vector<double>> data_after_inject;
    for (int i = 0; i < 1; i++)
    {
        data_before_inject.push_back(data_before_inject_temp[i]);
        data_after_inject.push_back(data_after_inject_temp[i]);
    }

    std::vector<std::vector<double>> data_res;
    for (auto chunk : data_before_inject)
    {
        Audio_frame frame(chunk);
        int samplerate = 44100;
        Parametrs_dwz parametrs_dwz = Parametrs_dwz(samplerate);
        process_frame_inject(frame, parametrs_dwz);
        data_res.push_back(frame.get_frame());
    }

    bool is_data_eqal = test_equals_data(data_after_inject, data_res);
    std::cout << "is_data_eqal = " << is_data_eqal << std::endl;
    std::cout << "program finished" << std::endl;
}
void test_inject_detect_function()
{
    std::string test_real_data_before_dct = "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/test_data/test_data_frame_before_inject.txt";

    auto data_before_inject_temp = read_all_data(test_real_data_before_dct);

    std::vector<std::vector<double>> data_before_inject;
    for (int i = 0; i < data_before_inject_temp.size(); i++)
    // for(int i =0;i<1;i++)
    {
        data_before_inject.push_back(data_before_inject_temp[i]);
    }

    std::vector<bool> data_res;
    for (auto chunk : data_before_inject)
    {
        Audio_frame frame(chunk);
        int samplerate = 44100;
        Parametrs_dwz parametrs_dwz = Parametrs_dwz(samplerate);

        auto start = std::chrono::steady_clock::now();
        process_frame_inject(frame, parametrs_dwz);
        bool res_detect = process_frame_extract(frame, parametrs_dwz);
        auto end = std::chrono::steady_clock::now();
        std::cout<< "time: "<< std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()<<" micro sec"<<std::endl;

        data_res.push_back(res_detect);
    }
    for(int i =0;i<data_res.size();i++)
    {
        if(data_res[i])
        {
            std::cout<<i<<") True"<<std::endl;
        }
        else
        {
            std::cout<<i<<") False"<<std::endl;
        }
    }
}
void test_extract_function()
{
    std::string test_real_data_before_dct = "/home/INTEXSOFT/alexander.polianski/work/video project/audio_wm/Scripts/C_code/test_data/test_data_frame_after_inject.txt";

    auto data_inject_temp = read_all_data(test_real_data_before_dct);

    std::vector<std::vector<double>> data_after_inject;
    for (int i = 0; i < data_inject_temp.size(); i++)
    //for(int i =0;i<1;i++)
    {
        data_after_inject.push_back(data_inject_temp[i]);
    }

    std::vector<bool> data_res;
    for (auto chunk : data_after_inject)
    {
        Audio_frame frame(chunk);
        int samplerate = 44100;
        Parametrs_dwz parametrs_dwz = Parametrs_dwz(samplerate);
        bool res_detect = process_frame_extract(frame, parametrs_dwz);
        data_res.push_back(res_detect);
    }
    for(int i =0;i<data_res.size();i++)
    {
        if(data_res[i])
        {
            std::cout<<i<<") True"<<std::endl;
        }
        else
        {
            std::cout<<i<<") False"<<std::endl;
        }
    }
}

