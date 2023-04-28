#include "Headers.h"
#include "data_wrapper.h"
#include "quality_param.h"
#include "scripts.h"
int main(int argc, char* argv[])
{
    std::cout << "program start" << std::endl;

    std::string key;
    if(argc > 1)
    {
        key = std::string(argv[1]);
    }
    

    if(key == std::string("-i")) // инжектор
    {
        std::cout<<"key: -i"<<std::endl;
        std::string input_file_name(argv[2]);
        std::string output_file_name(argv[3]);

        std::vector<std::vector<double>> streams;
        std::vector<Quality_param> quality_res;

        Parametrs_dwz param = read_streams(input_file_name, streams);

        std::cout<<"read_streams finish"<<std::endl;
        param.print();
        for(int stream_index = 0; stream_index <streams.size(); stream_index++)
        {
            Quality_param qual = process_inject(streams[stream_index], param);

            //qual.print_debug();// debug

            quality_res.push_back(qual);

            int res_detect = process_detect(streams[stream_index], param);
            std::cout<<"--> res_detect="<<res_detect<<std::endl;
        }
        

        write_streams(output_file_name, streams, quality_res);
    }



    // test_inject_function();
    //test_inject_detect_function();
    //test_extract_function();
    std::cout << "program finished" << std::endl;
    return 0;
}