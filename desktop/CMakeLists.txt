cmake_minimum_required(VERSION 3.30)

project(
  TurntableTools
  VERSION 0.1.0
  DESCRIPTION "This is a tool for setting up a record player."
  HOMEPAGE_URL "https://github.com/Jake-The-Human/Turntable-Tools"
  LANGUAGES CXX C
)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include("cmake/dependencies.cmake")

# ---- Declare library ----

add_library(
  TurntableTools_lib OBJECT
  source/tools/turntable_tools.hpp
  source/tools/turntable_tools.cpp
  source/tools/moving_avg.hpp
  source/tools/azimuth.hpp
  source/tools/azimuth.cpp
  source/tools/thd.hpp
  source/tools/thd.cpp
  source/tools/tracking_ability.hpp
  source/tools/tracking_ability.cpp
  source/tools/frequency_response.hpp
  source/tools/frequency_response.cpp
  source/tools/fft.hpp
  source/tools/fft.cpp
  source/tools/phase.hpp
  source/tools/phase.cpp
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

add_executable(TurntableTools_exe
  source/main.cpp
  source/dr_wav.c
  source/application.cpp
  source/audio_window.cpp
  source/dr_wav.h
  source/application.hpp
  source/audio_window.hpp
  ${imgui_SOURCE}
)

add_executable(TurntableTools::exe ALIAS TurntableTools_exe)
target_compile_definitions(TurntableTools_exe
  PRIVATE IMGUI_IMPL_OPENGL_LOADER_GLAD
)

set_property(TARGET TurntableTools_exe PROPERTY OUTPUT_NAME TurntableTools)

target_compile_features(TurntableTools_exe PRIVATE cxx_std_20)

target_link_libraries(TurntableTools_exe
  PRIVATE TurntableTools_lib
  OpenGL::OpenGL
  glfw
)

target_include_directories(TurntableTools_exe SYSTEM PRIVATE ${imgui_SOURCE_DIR} ${implot_SOURCE_DIR})

target_compile_definitions(TurntableTools_exe PRIVATE MA_NO_MP3)

add_subdirectory("${PROJECT_SOURCE_DIR}/test")

