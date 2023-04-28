#include "Audio_frame.h"

Audio_frame::Audio_frame() : _size(0) {};
Audio_frame::Audio_frame(int size) : _size(size)
{
    _frame.reserve(this->_size);
};
Audio_frame::Audio_frame(std::vector<double> vect)
{
    this->_size = vect.size();
    this->_frame = vect;
};
Audio_frame::~Audio_frame() {}
int Audio_frame::size() const
{
    return this->_size;
}

 double& Audio_frame::operator [] (int index)
 {
    return this->_frame[index];
 }

std::vector<double> Audio_frame::get_frame() const
{
    return this->_frame;
}
int Audio_frame::find_pos_abs_max() const
{
    if (this->_size == 0)
    {
        return 0; // вставить исключение
    }
    double pos_max = 0;
    double pos_min = 0;
    for (int i = 0; i < this->_size; i++)
    {
        if (_frame[i] > _frame[pos_max])
        {
            pos_max = i;
            continue;
        }
        if (_frame[i] < _frame[pos_min])
        {
            pos_min = i;
        }
    }
    int result = pos_max;
    if (std::abs(_frame[pos_min]) > std::abs(_frame[pos_max]))
    {
        result = pos_min;
    }
    return result;
}

double* get_array_part_frame(Audio_frame& frame, int pos_start, int pos_end)
{
    int n = pos_end - pos_start;
    double *in = new double[n];
    std::copy(frame._frame.begin() + pos_start, frame._frame.begin() + pos_end + 1, in);
    return in;
}

std::unique_ptr<double[]> get_array_part_frame_(Audio_frame& frame, int pos_start, int pos_end)
{
    int n = pos_end - pos_start;
    std::unique_ptr<double[]> ptr_frame = std::make_unique<double[]>(n);
    std::copy(frame._frame.begin() + pos_start, frame._frame.begin() + pos_end + 1, ptr_frame.get());
    return ptr_frame;
}