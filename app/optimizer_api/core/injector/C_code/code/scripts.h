#include "Audio_frame.h"
#include "Parametrs_dwz.h"
#include "quality_param.h"

bool process_frame_inject(Audio_frame &frame, const Parametrs_dwz &parametrs);
bool process_frame_extract(Audio_frame &frame, const Parametrs_dwz &parametrs);


bool internal_process_frame_inject_(Audio_frame &frame, const Parametrs_dwz &parametrs);

Quality_param process_inject(std::vector<double> &stream, const Parametrs_dwz &parametrs);
int process_detect(std::vector<double> &raw_stream, const Parametrs_dwz &parametrs);