#include "Headers.h"
#include "Audio_frame.h"

std::vector<double> dct(std::vector<double>& vect);
std::vector<double> idct(std::vector<double>& vect);
std::vector<double> dct_part_frame(Audio_frame& frame, int pos_start, int pos_end);

std::unique_ptr<double[]> dct_part_frame_(Audio_frame& frame, int pos_start, int pos_end);
std::unique_ptr<double[]> idct(std::unique_ptr<double[]>& in, int size);