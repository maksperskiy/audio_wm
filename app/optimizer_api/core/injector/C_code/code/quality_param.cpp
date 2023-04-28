#include "quality_param.h"
#include "common.h"
#include <cmath>

double calculate_SNR(const std::vector<double> &raw_signal, const std::vector<double> &marked_signal)
{
    int test_equal = 0;
    int test_not_equal = 0;


    double res = 0.0;
    double noise = 0.0;
    double max_raw_signal = find_abs_max(raw_signal, 0, raw_signal.size());
    // double max_marked_signal = find_abs_max(marked_signal, 0, marked_signal.size());
    double A = 0.0;
    double N = 0.0;
    for (int i = 0; i < marked_signal.size(); i++)
    {
        A += (raw_signal[i] / max_raw_signal) * (raw_signal[i] / max_raw_signal);
        N += ((raw_signal[i] - marked_signal[i]) / max_raw_signal) * ((raw_signal[i] - marked_signal[i]) / max_raw_signal);
    }
    
    //std::cout<<" calculate_SNR; max_raw_signal="<<max_raw_signal<<"; A= "<<A<<"; N ="<<N<<std::endl;
    //std::cout<<" calculate_SNR; test_equal="<<test_equal<<"; test_not_equal= "<<test_not_equal<<std::endl;

    A = sqrt(A);
    N = sqrt(N);

    std::cout<<" calculate_SNR; A= "<<A<<"; N ="<<N<<std::endl;
    
    // TODO: деление на ноль, если мы вообще не меняли сигнал
    return 10 * log10((A / N) * (A / N));
}

Quality_param::Quality_param(int count_fragment_for_inject_dwm, int count_inject_dwm, const std::vector<double> &input, const std::vector<double> &output)
{
    this->count_fragment_for_inject_dwm = count_fragment_for_inject_dwm;
    this->count_inject_dwm = count_inject_dwm;
    this->SNR = calculate_SNR(input, output);
}

void Quality_param::print_debug()
{
    std::cout<<"max_count_dwm="<<this->count_fragment_for_inject_dwm<<"; inject_count_dwm="<< this->count_inject_dwm<<"; SNR ="<<this->SNR<<std::endl;

}

double Quality_param::get_SNR()
{
    return this->SNR;
}
int Quality_param::get_count_max_dwm()
{
    return this->count_fragment_for_inject_dwm;
}
int Quality_param::get_count_inject_dwm()
{
    return this->count_inject_dwm;
}