#include "Headers.h"


class Audio_param_exception: public std::exception
{
public:
    Audio_param_exception(const std::string& message): message{message}
    {}
    const char* what() const noexcept override
    {
        return message.c_str();     // получаем из std::string строку const char*
    }
private:
    std::string message;    // сообщение об ошибке
};
