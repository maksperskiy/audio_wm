#include "dct_function.h"
#include <fftw3.h>

std::vector<double> dct_internal(int size, double* in)
{
    double *out = new double[size];

    fftw_plan plan = fftw_plan_r2r_1d(size, in, out, FFTW_REDFT10, FFTW_ESTIMATE);
    fftw_execute(plan);
    std::vector<double> res;
    res.reserve(size);
    for (int i = 0; i < size; i++)
    {
        res.push_back(out[i]);
    }
    delete[] out;
    fftw_destroy_plan(plan);
    fftw_cleanup();
    return res;
}
std::unique_ptr<double[]> dct_internal_(int size, double* in)
{
    std::unique_ptr<double[]> out = std::make_unique<double[]>(size);

    fftw_plan plan = fftw_plan_r2r_1d(size, in, out.get(), FFTW_REDFT10, FFTW_ESTIMATE);
    fftw_execute(plan);
    fftw_destroy_plan(plan);
    fftw_cleanup();
    return out;
}

std::vector<double> dct_internal_reverse(int size, double* in)
{
    double *out = new double[size];

    fftw_plan plan = fftw_plan_r2r_1d(size, in, out, FFTW_REDFT01, FFTW_ESTIMATE);
    fftw_execute(plan);
    std::vector<double> res;
    res.reserve(size);
    for (int i = 0; i < size; i++)
    {
        // нормируем значения
        res.push_back(out[i]/(2*(size - 1)));
    }
    delete[] out;
    fftw_destroy_plan(plan);
    fftw_cleanup();
    return res;
}
std::unique_ptr<double[]> dct_internal_reverse_(int size, double* in)
{
    std::unique_ptr<double[]> out = std::make_unique<double[]>(size);

    fftw_plan plan = fftw_plan_r2r_1d(size, in, out.get(), FFTW_REDFT01, FFTW_ESTIMATE);
    fftw_execute(plan);
    for (int i = 0; i < size; i++)
    {
        // нормируем значения
        out[i] = (out[i]/(2*(size - 1)));
    }
    fftw_destroy_plan(plan);
    fftw_cleanup();
    return out;
}
std::vector<double> dct(std::vector<double>& vect)
{
    int n = vect.size();
    double *in = new double[n];
    
    std::copy(vect.begin(), vect.end(), in);
    auto res = dct_internal(n, in);
    delete [] in;
    return res;
}


std::vector<double> idct(std::vector<double>& vect)
{
    int n = vect.size();
    double *in = new double[n];
    
    std::copy(vect.begin(), vect.end(), in);
    auto res = dct_internal_reverse(n, in);
    delete [] in;
    return res;
}

std::vector<double> dct_part_frame(Audio_frame& frame, int pos_start, int pos_end)
{
    int n = pos_end - pos_start;
    double *in = get_array_part_frame(frame, pos_start, pos_end);
    auto res = dct_internal(n,in);
    delete [] in;
    return res;
}

std::unique_ptr<double[]> dct_part_frame_(Audio_frame& frame, int pos_start, int pos_end)
{
    int n = pos_end - pos_start;

    std::unique_ptr<double[]> ptr_frame = get_array_part_frame_(frame, pos_start, pos_end);
    return dct_internal_(n, ptr_frame.get());
}

std::unique_ptr<double[]> idct(std::unique_ptr<double[]>& in, int size)
{
    return dct_internal_reverse_(size, in.get());
}