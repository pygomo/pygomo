cmake_minimum_required(VERSION 3.16)
project(pygomo CXX)

set(CMAKE_CXX_STANDARD          11  CACHE STRING "The C++ standard whose features are requested to build this target.")
set(CMAKE_CXX_STANDARD_REQUIRED ON  CACHE BOOL "Boolean describing whether the value of CXX_STANDARD is a requirement.")
set(CMAKE_CXX_EXTENSIONS        OFF CACHE BOOL "Boolean specifying whether compiler specific extensions are requested.")

set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "Boolean specifying whether to build the GLFW example programs.")
set(GLFW_BUILD_TESTS    OFF CACHE BOOL "Boolean specifying whether to build the GLFW test programs.")
set(GLFW_BUILD_DOCS     OFF CACHE BOOL "Boolean specifying whether to build the GLFW documentation.")

set(BUILD_SHARED_LIBS ON CACHE BOOL "Boolean telling add_library() to default to SHARED libraries.")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_subdirectory("extern/pybind11")
add_subdirectory("extern/glew")
add_subdirectory("extern/glfw")

include_directories("extern/pybind11/include")
include_directories("extern/glew/include")
include_directories("extern/glfw/include")
