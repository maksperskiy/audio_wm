#include "common.h"

void reset_same_part(std::vector<double> &frame, int start, int count)
{
    for (int i = 0; i < count; i++)
    {
        frame[start + i] = 0;
    }
}
void multiplier_same_part(std::vector<double> &frame, int start, int count, double multiplier)
{
    for (int i = 0; i < count; i++)
    {
        frame[start + i] *= multiplier;
    }
}
double find_abs_max(const std::vector<double> &frame, int start, int count)
{
    double max = std::abs(frame[start]);
    for (int i = 0; i < count; i++)
    {
        if (max < std::abs(frame[start + i]))
        {
            max = std::abs(frame[start + i]);
        }
    }
    return max;
}
///////////
void reset_same_part(double *frame, int start, int count)
{
    for (int i = 0; i < count; i++)
    {
        frame[start + i] = 0;
    }
}
void multiplier_same_part(double *frame, int start, int count, double multiplier)
{
    for (int i = 0; i < count; i++)
    {
        frame[start + i] *= multiplier;
    }
}
double find_abs_max(double *frame, int start, int count)
{
    double max = std::abs(frame[start]);
    for (int i = 0; i < count; i++)
    {
        if (max < std::abs(frame[start + i]))
        {
            max = std::abs(frame[start + i]);
        }
    }
    return max;
}
////////