#include "Parametrs_dwz.h"

int Parametrs_dwz::get_radius_extremum() const
{
    return (int)(this->_duration * this->_samplerate / 2000); // /1000 для мс и /2 для радиуса
}
int Parametrs_dwz::get_samplerate() const
{
    return this->_samplerate;
}
int Parametrs_dwz::get_bottom_freq() const
{
    return this->bottom_freq;
}
int Parametrs_dwz::get_top_freq() const
{
    return this->top_freq;
}
int Parametrs_dwz::get_count_bit_DWZ() const
{
    return this->count_bit_DWZ;
}
int Parametrs_dwz::get_dwz_bit(int index) const
{
    return (this->dwz >> index) & 1;
}
Parametrs_dwz::Parametrs_dwz(int samplerate)
{
    this->_samplerate = samplerate;
    this->_duration = 20;
    this->radius_extremum;
    this->bottom_freq = 1750;
    this->top_freq = 8500;
    this->dwz = 0x123456;
    this->count_bit_DWZ;
    this->N = 100000;
    expand();
}
Parametrs_dwz::Parametrs_dwz(int samplerate, double duration, int bottom_freq, int top_freq, uint64_t dvm, int N)
{
    this->_samplerate = samplerate;
    this->_duration = duration;
    this->radius_extremum = 0;
    this->bottom_freq = bottom_freq;
    this->top_freq = top_freq;
    this->dwz = dvm;
    this->count_bit_DWZ;
    this->N = N;
    expand();
}
Parametrs_dwz::Parametrs_dwz() : Parametrs_dwz(44100){};
int Parametrs_dwz::calculate_count_byte()
{
    int count = 0;
    auto temp = this->dwz;
    while (temp)
    {
        temp = temp >> 8;
        count++;
    }
    return count * 8;
}
void Parametrs_dwz::expand()
{
    int count_byte_DWM = calculate_count_byte() / 8;
    uint8_t check_byte_1 = 0;
    uint8_t check_byte_2 = 0;
    uint64_t temp_dwm = this->dwz;
    for (int i = 0; i < count_byte_DWM; i++)
    {
        check_byte_1 ^= (temp_dwm >> i * 8) & 0xff;
        check_byte_2 |= (temp_dwm >> i * 8) & 0xff;
    }
    this->dwz = temp_dwm << 16 | check_byte_1 << 8 | check_byte_2;
    this->count_bit_DWZ = count_byte_DWM * 8 + 16;
}
int Parametrs_dwz::get_N() const
{
    return this->N;
}
bool Parametrs_dwz::is_check_bit(uint64_t mess) const
{
    bool res = false;
    uint64_t check_byte_1 = 0;
    uint64_t check_byte_2 = 0;
    int count_b = (count_bit_DWZ - 16) / 8;
    uint64_t main_part = mess >> 16;
    for(int i = 0; i < count_b; i++)
    {
        check_byte_1 = check_byte_1 ^ ((main_part >> i*8)&0xff);
        check_byte_2 = check_byte_2 | ((main_part >> i*8)&0xff);
    }
    return (mess & 0xffff) == ((check_byte_1<<8) | check_byte_2);
}

uint64_t Parametrs_dwz::get_dvm() const
{
    return  this->dwz >> 16;
}


// test
void Parametrs_dwz::print() const
{
    std::cout<<"------ dwm parametrs -----"<< std::endl;
    std::cout<<"samplerate="<< _samplerate<< std::endl;
    std::cout<<"duration= "<< _duration<< std::endl;
    std::cout<<"radius_extremum="<< radius_extremum << std::endl;
    std::cout<<"bottom_freq="<< bottom_freq<< std::endl;
    std::cout<<"top_freq="<< top_freq<< std::endl;
    std::cout<<"dwz="<<dwz<< std::endl;
    std::cout<<"count_bit_DWZ="<< count_bit_DWZ<< std::endl;
    std::cout<<"N="<< N<< std::endl;
    std::cout<<"--------------- "<<std::endl;
}
