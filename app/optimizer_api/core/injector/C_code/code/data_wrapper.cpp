#include "data_wrapper.h"

Parametrs_dwz read_streams(std::string file_name, std::vector<std::vector<double>> &streams)
{
    std::ifstream input(file_name);

    streams.clear();
    int count_stream = 0;
    int counter = 0;
    double numb = 0.0;
    //std::vector<double> stream;

    input >> count_stream;
    std::cout << " count_stream=" << count_stream << std::endl;
    for (int j = 0; j < count_stream; j++)
    {
        input >> counter;
        std::cout << " counter=" << counter << std::endl;
        // stream.clear();
        // stream.resize(counter);
        std::vector<double> stream;
        for (int i = 0; i < counter; i++)
        {
            input >> numb;
            stream.push_back(numb);
        }
        streams.push_back(stream);
    }
    int samplerate;
    input >> samplerate;
    std::cout << " samplerate=" << samplerate << std::endl;
    double duration;
    input >> duration;
    std::cout << " duration=" << duration << std::endl;
    int bottom_freq;
    input >> bottom_freq;
    std::cout << " bottom_freq=" << bottom_freq << std::endl;
    int top_freq;
    input >> top_freq;
    std::cout << " top_freq=" << top_freq << std::endl;
    uint64_t dwm;
    input >> dwm;
    std::cout << " dvm=" << dwm << std::endl;
    int N;
    input >> N;
    std::cout << " N=" << N << std::endl;

    input.clear();
    input.close();

    return Parametrs_dwz(samplerate, duration, bottom_freq, top_freq, dwm, N);
}

void write_stream(std::string file_name, std::vector<double> &stream, Quality_param &param)
{
    std::ofstream out(file_name, std::ios::out);
    out << param.get_count_max_dwm() << std::endl;
    out << param.get_count_inject_dwm() << std::endl;
    out << param.get_SNR() << std::endl;
    for (auto i : stream)
    {
        out << i << ' ';
    }
    out.close();
}

void write_streams(std::string file_name, std::vector<std::vector<double>> &stream, std::vector<Quality_param> &param)
{
    std::ofstream out(file_name, std::ios::out);

    int count_stream = param.size();
    out << count_stream << std::endl;
    for (int i = 0; i < count_stream; i++)
    {
        out << param[i].get_count_max_dwm() << std::endl;
        out << param[i].get_count_inject_dwm() << std::endl;
        out << param[i].get_SNR() << std::endl;
        for (auto i : stream[i])
        {
            out << i << ' ';
        }
        out<<std::endl;
    }
    out.close();
}