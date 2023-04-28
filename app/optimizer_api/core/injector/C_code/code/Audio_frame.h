#pragma once
#include "Headers.h"

class Audio_frame
{
    int _size;
    std::vector<double> _frame;

    Audio_frame(const Audio_frame &) = delete;
    friend double* get_array_part_frame(Audio_frame& frame, int pos_start, int pos_end);
    friend std::unique_ptr<double[]> get_array_part_frame_(Audio_frame& frame, int pos_start, int pos_end);
public:
    Audio_frame();
    Audio_frame(int size);
    Audio_frame(std::vector<double> vect);
    ~Audio_frame();
    int size() const;
    int samplerate() const;
    int find_pos_abs_max() const;
    double& operator [] (int index);
    std::vector<double> get_frame() const;
};

