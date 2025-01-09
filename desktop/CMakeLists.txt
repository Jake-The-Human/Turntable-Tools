cmake_minimum_required(VERSION 3.30)

project(
    TurntableTools
    VERSION 0.1.0
    DESCRIPTION "This is a tool for setting up a record player."
    HOMEPAGE_URL "https://github.com/Jake-The-Human/Turntable-Tools"
    LANGUAGES CXX C
)

include("cmake/dependencies.cmake")

# ---- Declare library ----

add_library(
    TurntableTools_lib OBJECT
    source/turntable_tools.cpp
    source/azimuth.hpp
    source/azimuth.cpp
    source/thd.hpp
    source/thd.cpp
    source/tracking_ability.hpp
    source/tracking_ability.cpp
    source/frequency_response.hpp
    source/frequency_response.cpp
    source/fft.hpp
    source/fft.cpp
    source/phase.hpp
    source/phase.cpp
    source/constants.hpp
    )

target_include_directories(
    TurntableTools_lib ${warning_guard}
    PUBLIC
    "\$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/source>"
    PRIVATE
    ${pocketfft_SOURCE_DIR}
)

# target_link_libraries(TurntableTools_lib PRIVATE PocketFFT)

target_compile_features(TurntableTools_lib PUBLIC cxx_std_20)

# ---- Declare executable ----

add_executable(TurntableTools_exe source/main.cpp source/miniaudio.cpp)
add_executable(TurntableTools::exe ALIAS TurntableTools_exe)

set_property(TARGET TurntableTools_exe PROPERTY OUTPUT_NAME TurntableTools)

target_compile_features(TurntableTools_exe PRIVATE cxx_std_20)

target_link_libraries(TurntableTools_exe PRIVATE TurntableTools_lib PRIVATE argparse)

target_include_directories(TurntableTools_exe SYSTEM PRIVATE ${miniaudio_SOURCE_DIR})

target_compile_definitions(TurntableTools_exe
  PRIVATE MA_NO_MP3
  PRIVATE ARGPARSE_BUILD_SAMPLES=OFF
  PRIVATE ARGPARSE_BUILD_TESTS=OFF)

add_subdirectory("${PROJECT_SOURCE_DIR}/test")

