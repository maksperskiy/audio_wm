#include "Headers.h"

void reset_same_part(std::vector<double> &frame, int start, int count);
void multiplier_same_part(std::vector<double> &frame, int start, int count, double multiplier);
double find_abs_max(const std::vector<double> &frame, int start, int count);
///////////
void reset_same_part(double *frame, int start, int count);
void multiplier_same_part(double *frame, int start, int count, double multiplier);
double find_abs_max(double *frame, int start, int count);
///////////