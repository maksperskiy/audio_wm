#pragma once
#include "Headers.h"

class Parametrs_dwz
{
    int _samplerate;
    double _duration;
    int radius_extremum;
    int bottom_freq;
    int top_freq;
    uint64_t dwz;
    int count_bit_DWZ;
    int N;

    void expand();
    int calculate_count_byte();

public:
    Parametrs_dwz();
    Parametrs_dwz(int samplerate);
    Parametrs_dwz(int samplerate, double duration, int bottom_freq, int top_freq, uint64_t dvm, int N);
    Parametrs_dwz(const Parametrs_dwz&) =default;
    int get_radius_extremum() const;
    int get_samplerate() const;
    int get_bottom_freq() const;
    int get_top_freq() const;
    int get_count_bit_DWZ() const;
    int get_dwz_bit(int index) const;
    bool is_check_bit(uint64_t mess) const;
    int get_N() const;
    uint64_t get_dvm() const;

    void print() const;
};