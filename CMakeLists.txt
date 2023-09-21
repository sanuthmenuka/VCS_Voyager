cmake_minimum_required(VERSION 3.26)
project(VCS_Voyager)

set(CMAKE_CXX_STANDARD 17)

add_executable(VCS_Voyager main.cpp)

find_package(Boost 1.82.0 REQUIRED CONFIG)
if(Boost_FOUND)
    message("Boost_INCLUDE_DIRS=${Boost_INCLUDE_DIRS}")
    include_directories(${Boost_INCLUDE_DIRS})
endif()

set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} /opt/local/lib)
find_package(PkgConfig REQUIRED)

pkg_check_modules(cryptopp REQUIRED )

find_package(cryptopp REQUIRED)
if(cryptopp_FOUND)
    message("cryptopp_INCLUDE_DIRS=${cryptopp_INCLUDE_DIRS}")
    include_directories(/opt/local/include/cryptopp)
endif ()

