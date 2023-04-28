#pragma once
#include "Headers.h"

class Quality_param
{
    int count_fragment_for_inject_dwm;
    int count_inject_dwm;
    double SNR;
    
    public:
    Quality_param() = default;
    Quality_param(int count_fragment_for_inject_dwm, int count_inject_dwm,const std::vector<double>& input,const std::vector<double>& output);
    Quality_param(const Quality_param&) = default;
    double get_SNR();
    int get_count_max_dwm();
    int get_count_inject_dwm();
    void print_debug();
};