cmake_minimum_required(VERSION 3.0)
project(testIMU)

include_directories(.)
link_directories(.)
# include_directories(/home/hi/workspace/SLAM-OB/Thirdparty/eigen3)
add_executable (imucal demo.cpp)
target_link_libraries (imucal libimucal.so )
