cmake_minimum_required(VERSION 3.19)
project(CeasorHash)

#set(CMAKE_PREFIX_PATH "C:/Users/Computer/AppData/Local/Programs/Python/Python310/Lib/site-packages/pybind11/include")
#set(CMAKE_PREFIX_PATH "C:/Users/Computer/AppData/Local/Programs/Python/Python310/Lib/site-packages/pybind11/share/cmake/pybind11")
#set(Python3_LIBRARIES "C:/Users/Computer/AppData/Local/Programs/Python/Python310/libs/python310.lib")

# python, pybind11 경로 설정
find_package(Python3 REQUIRED) # find_package: not work -> include_directories()
#find_package(pybind11 REQUIRED) # pip install pybind11로 설치한 pybind11의 경로를 자동으로 찾아줌
#add_subdirectory(pybind11)

# 헤더 파일 경로 추가
include_directories("C:/Users/Computer/Desktop/VS Code/project T") # encrypted_with_FNV1A.hh및 기타 헤더 파일의 경로
include_directories("C:/Users/Computer/AppData/Local/Programs/Python/Python310/Lib/site-packages/pybind11/include") # pybind11.h, stl.h
include_directories("C:/Users/Computer/AppData/Local/Programs/Python/Python310/include") # Python.h
link_directories("C:/Users/Computer/AppData/Local/Programs/Python/Python310/libs") # Python310.lib

# C++ 소스 파일과 pybind11을 함께 컴파일
add_library(CeasorHash MODULE wrapper.cpp) # compile wrapper.cpp to module
#pybind11_add_module(CeasorHash MODULE encrypt_with_fnv.hh)

# 파이썬 빌드를 위한 추가 설정 (라이브러리와 플래그)
#target_link_libraries(CeasorHash PRIVATE Python3::Python)

set(CMAKE_CXX_STANDARD 17)