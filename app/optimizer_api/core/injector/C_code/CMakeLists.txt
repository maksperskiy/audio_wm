cmake_minimum_required(VERSION 3.13)

project(video_test) #Project name

SET(CMAKE_CXX_COMPILER g++)
set(CMAKE_CXX_STANDARD 14) #setting C++ 14 standard

SET(CMAKE_BUILD_TYPE Release)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin/Release)

#SET(CMAKE_BUILD_TYPE Debug)
#set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin/Debug)

set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++")

# собираются все файлы по шаблону
file(GLOB CPP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/code/*.cpp")
#${CPP_SOURCES}
add_executable(${PROJECT_NAME} ${CPP_SOURCES})
target_link_libraries(${PROJECT_NAME} fftw3 )
#linking Gstreamer library with target executable
#target_link_libraries(${PROJECT_NAME} ${FFTW_LIBRARIES})