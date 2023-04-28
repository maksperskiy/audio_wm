#include "Headers.h"
#include "Audio_frame.h"
#include "Parametrs_dwz.h"
#include "quality_param.h"
#include<fstream>

Parametrs_dwz read_streams(std::string file_name, std::vector<std::vector<double>> &streams);
void write_stream(std::string file_name, std::vector<double>& stream, Quality_param& param);

void write_streams(std::string file_name, std::vector<std::vector<double>> &stream, std::vector<Quality_param> &param);