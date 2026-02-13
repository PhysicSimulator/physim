cmake_minimum_required(VERSION 3.25)
project(physim_installed_consumer LANGUAGES CXX)

find_package(physim CONFIG REQUIRED)

add_executable(consumer main.cpp)
target_link_libraries(consumer PRIVATE physim::physim)
