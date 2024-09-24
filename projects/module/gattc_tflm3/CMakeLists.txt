cmake_minimum_required(VERSION 3.5)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(test4)

# Add compiler flags globally (this will apply to all components)
add_compile_options(-Wno-error=switch -Wno-error=jump-misses-init)