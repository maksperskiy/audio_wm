#include "Headers.h"
#include "custom_exception.h"
#include "dct_function.h"
#include "scripts.h"
#include "common.h"


void prepare_frame_(Audio_frame &frame, const Parametrs_dwz &parametrs, int &size, int &pos_freq, int &bfi, int &interval_len, std::unique_ptr<double[]> &ptr)
{
    int extremum_pos = frame.find_pos_abs_max();
    int extremum_radius = parametrs.get_radius_extremum();

    int pos_top = extremum_pos + extremum_radius;
    pos_freq = extremum_pos - extremum_radius;

    if (pos_top > frame.size())
    {
        throw Audio_param_exception("pos_top=" + std::to_string(pos_top) + "; frame.size()=" + std::to_string(frame.size()));
    }
    if (pos_freq < 0)
    {
        throw Audio_param_exception("Audio_param_exception pos_freq=" + std::to_string(pos_freq));
    }
    if (pos_top == pos_freq)
    {
        throw Audio_param_exception("pos_top == pos_freq==" + std::to_string(pos_top));
    }

    ptr = dct_part_frame_(frame, pos_freq, pos_top);

    size = pos_top - pos_freq;
    double points_per_freq = (2 * size) / (double)parametrs.get_samplerate();
    bfi = points_per_freq * parametrs.get_bottom_freq();
    int tfi = points_per_freq * parametrs.get_top_freq();
    interval_len = (tfi - bfi) / parametrs.get_count_bit_DWZ();
    if (interval_len < 2)
    {
        throw Audio_param_exception("interval_len < 2; interval_len=" + std::to_string(interval_len));
    }

    // зануление некоторых частот
    reset_same_part(ptr.get(), 0, bfi - 1);
    reset_same_part(ptr.get(), tfi + 1, size - tfi - 1);
}

void prepare_frame(Audio_frame &frame, const Parametrs_dwz &parametrs, int &pos_freq, int &bfi, int &interval_len, std::vector<double> &dct_result)
{
    int extremum_pos = frame.find_pos_abs_max();
    int extremum_radius = parametrs.get_radius_extremum();

    int pos_top = extremum_pos + extremum_radius;
    pos_freq = extremum_pos - extremum_radius;

    //std::cout<<"pos_freq=" <<pos_freq<<"; pos_top="<<pos_top<<"; extremum_radius="<<extremum_radius<<std::endl;
    if (pos_top > frame.size())
    {
        throw Audio_param_exception("pos_top=" + std::to_string(pos_top) + "; frame.size()=" + std::to_string(frame.size()));
    }
    if (pos_freq < 0)
    {
        throw Audio_param_exception("Audio_param_exception pos_freq=" + std::to_string(pos_freq));
    }
    if (pos_top == pos_freq)
    {
        throw Audio_param_exception("pos_top == pos_freq==" + std::to_string(pos_top));
    }

    dct_result = dct_part_frame(frame, pos_freq, pos_top);

    double points_per_freq = (2 * (pos_top - pos_freq)) / (double)parametrs.get_samplerate();
    bfi = points_per_freq * parametrs.get_bottom_freq();
    int tfi = points_per_freq * parametrs.get_top_freq();
    interval_len = (tfi - bfi) / parametrs.get_count_bit_DWZ();
    if (interval_len < 2)
    {
        throw Audio_param_exception("interval_len < 2; interval_len=" + std::to_string(interval_len));
    }

    // зануление некоторых частот
    reset_same_part(dct_result, 0, bfi - 1);
    reset_same_part(dct_result, tfi + 1, dct_result.size() - tfi - 1);
}

bool internal_process_frame_inject_(Audio_frame &frame, const Parametrs_dwz &parametrs)
{
    int bfi = 0;
    int interval_len = 0;
    int pos_freq = 0;
    int size = 0;
    std::unique_ptr<double[]> ptr;

    prepare_frame_(frame, parametrs, size, pos_freq, bfi, interval_len, ptr);
    int midle = interval_len / 2;

    for (int interval_index = 0; interval_index < parametrs.get_count_bit_DWZ(); interval_index++)
    {
        int pos_begin_inteval = bfi + interval_index * interval_len;
        int bit = parametrs.get_dwz_bit(interval_index);

        double abs_left_max = find_abs_max(ptr.get(), pos_begin_inteval, midle);
        double abs_right_max = find_abs_max(ptr.get(), pos_begin_inteval + midle, interval_len - midle);
        double abs_interval_max = abs_right_max > abs_left_max ? abs_right_max : abs_left_max;
        abs_left_max /= abs_interval_max;
        abs_right_max /= abs_interval_max;

        if (bit)
        {
            reset_same_part(ptr.get(), pos_begin_inteval + midle, interval_len - midle);
            multiplier_same_part(ptr.get(), pos_begin_inteval, midle, abs_left_max);
        }
        else
        {
            reset_same_part(ptr.get(), pos_begin_inteval, midle);
            multiplier_same_part(ptr.get(), pos_begin_inteval + midle, interval_len - midle, abs_right_max);
        }

        abs_left_max = find_abs_max(ptr.get(), pos_begin_inteval, midle);
        abs_right_max = find_abs_max(ptr.get(), pos_begin_inteval + midle, interval_len - midle);
        int res_embed = abs_left_max > abs_right_max ? 1 : 0;
        if (res_embed != bit)
        {
            return false;
        }
    }

    auto idct_res = idct(ptr, size);

    for (int i = 0; i < size; i++)
    {
        frame[pos_freq + i] -= idct_res[i];
    }

    return true;
}

bool internal_process_frame_inject(Audio_frame &frame, const Parametrs_dwz &parametrs)
{
    int bfi = 0;
    int interval_len = 0;
    int pos_freq = 0;

    std::vector<double> dct_result;
    prepare_frame(frame, parametrs, pos_freq, bfi, interval_len, dct_result);
    int midle = interval_len / 2;

    //std::cout<<"interval_len="<<interval_len<<std::endl;
    //std::cout<<"pos_freq==="<<pos_freq<<"; frame[pos_freq]"<<frame[pos_freq]<<std::endl;
    //std::cout<<"pos_top==="<<pos_freq + interval_len<<"; frame[pos_top]"<<frame[pos_freq + interval_len]<<std::endl;

    for (int interval_index = 0; interval_index < parametrs.get_count_bit_DWZ(); interval_index++)
    {
        int pos_begin_inteval = bfi + interval_index * interval_len;
        int bit = parametrs.get_dwz_bit(interval_index);

        double abs_left_max = find_abs_max(dct_result, pos_begin_inteval, midle);
        double abs_right_max = find_abs_max(dct_result, pos_begin_inteval + midle, interval_len - midle);
        double abs_interval_max = abs_right_max > abs_left_max ? abs_right_max : abs_left_max;
        abs_left_max /= abs_interval_max;
        abs_right_max /= abs_interval_max;

        if (bit)
        {
            reset_same_part(dct_result, pos_begin_inteval + midle, interval_len - midle);
            multiplier_same_part(dct_result, pos_begin_inteval, midle, abs_left_max);
        }
        else
        {
            reset_same_part(dct_result, pos_begin_inteval, midle);
            multiplier_same_part(dct_result, pos_begin_inteval + midle, interval_len - midle, abs_right_max);
        }

        abs_left_max = find_abs_max(dct_result, pos_begin_inteval, midle);
        abs_right_max = find_abs_max(dct_result, pos_begin_inteval + midle, interval_len - midle);
        int res_embed = abs_left_max > abs_right_max ? 1 : 0;
        if (res_embed != bit)
        {
            return false;
        }
    }

    auto idct_res = idct(dct_result);

    for (int i = 0; i < idct_res.size(); i++)
    {
        frame[pos_freq + i] -= idct_res[i];
    }

    return true;
}

bool internal_process_frame_extract(Audio_frame &frame, const Parametrs_dwz &parametrs)
{
    int bfi = 0;
    int interval_len = 0;
    int pos_freq = 0;
    std::vector<double> dct_result;
    prepare_frame(frame, parametrs, pos_freq, bfi, interval_len, dct_result);
    int midle = interval_len / 2;

    uint64_t res = 0;
    for (int interval_index = 0; interval_index < parametrs.get_count_bit_DWZ(); interval_index++)
    {
        int pos_begin_inteval = bfi + interval_index * interval_len;

        double abs_left_max = find_abs_max(dct_result, pos_begin_inteval, midle);
        double abs_right_max = find_abs_max(dct_result, pos_begin_inteval + midle, interval_len - midle);
        uint64_t bit = abs_right_max > abs_left_max ? 1 : 0;
        res = res | (bit << interval_index);
    }

    
    return parametrs.is_check_bit(res);// после обсуждения решено проверять имено по контрольным битам
}

bool process_frame_inject(Audio_frame &frame, const Parametrs_dwz &parametrs)
{
    bool res = false;
    try
    {
        res = internal_process_frame_inject(frame, parametrs);
    }
    catch (Audio_param_exception ex)
    {
        std::cout << ex.what() << std::endl;
    }
    // TODO: добавить обработку ошибок
    // catch(...)
    // {
    //     std::cout << ex.what() << std::endl;
    // }
    return res;
}

bool process_frame_extract(Audio_frame &frame, const Parametrs_dwz &parametrs)
{
    bool res = false;
    try
    {
        res = internal_process_frame_extract(frame, parametrs);
    }
    catch (Audio_param_exception ex)
    {
        std::cout << ex.what() << std::endl;
    }
    return res;
}


Quality_param process_inject(std::vector<double> &raw_stream, const Parametrs_dwz &parametrs)
{
    std::vector<double> stream(raw_stream);

    int size = stream.size();
    int N = parametrs.get_N();
    int count_fragment_for_inject_dwz = size / N;
    if (size / N != 0)
    {
        count_fragment_for_inject_dwz++;
    }
    int succes = 0;
    for (int index_fragment = 0; index_fragment < count_fragment_for_inject_dwz; index_fragment++)
    {
        int fragment_start = index_fragment * N;
        int fragment_end = (index_fragment + 1) * N;
        if (fragment_end > size)
        {
            fragment_end = size;
        }
        int len = fragment_end - fragment_start;
        std::vector<double> temp_frame;
        temp_frame.reserve(len);
        int y_counter =0;
        for(int j =0;j<len;j++)
        {
            temp_frame.push_back(stream[fragment_start+j]);
        }
        Audio_frame frame(temp_frame);
        
        if (process_frame_inject(frame, parametrs) && process_frame_extract(frame, parametrs))
        //if (process_frame_inject(frame, parametrs))
        {     
            succes++;
            for (int i = 0; i < len; i++)
            {
                stream[fragment_start + i] = frame[i];
            }

             std::vector<double> temp_frame_temp;
             temp_frame_temp.reserve(frame.size());
             for(int j = 0; j < frame.size(); j++)
             {
                temp_frame_temp.push_back(stream[fragment_start + j]);
             }

            Audio_frame frame_test(temp_frame_temp);
        }
    }

    std::cout<<" > injected: "<<succes<<std::endl;
    Quality_param qual_param = Quality_param(count_fragment_for_inject_dwz, succes, raw_stream, stream);
    raw_stream = stream;
    return qual_param;
}

int process_detect(std::vector<double> &raw_stream, const Parametrs_dwz &parametrs)
{
    int size = raw_stream.size();
    int N = parametrs.get_N();
    int count_fragment_for_inject_dwz = size / N;
    if (size / N != 0)
    {
        count_fragment_for_inject_dwz++;
    }
    int succes = 0;
    for (int index_fragment = 0; index_fragment < count_fragment_for_inject_dwz; index_fragment++)
    {
        int fragment_start = index_fragment * N;
        int fragment_end = (index_fragment + 1) * N;
        if (fragment_end > size)
        {
            fragment_end = size;
        }
        int len = fragment_end - fragment_start;
        std::vector<double> temp_frame;
        temp_frame.reserve(len);
        int y_counter =0;
        for(int j =0;j<len;j++)
        {
            temp_frame.push_back(*(raw_stream.begin()+ fragment_start +j));
        }

        Audio_frame frame(temp_frame);
        if (process_frame_extract(frame, parametrs))
        {     
            succes++;
        }
       
    }
    return succes;
}