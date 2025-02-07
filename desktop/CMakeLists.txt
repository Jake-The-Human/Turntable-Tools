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

set(turntable_tools_SOURCE
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

set(third_party_SOURCE
  source/third_party/dr_wav.c
  source/third_party/dr_wav.h
  source/third_party/toml.hpp
)

add_executable(TurntableTools_exe
  source/main.cpp
  source/app_state.cpp
  source/audio_data.cpp
  source/application.cpp
  source/audio_window.cpp
  source/azimuth_window.cpp
  source/thd_window.cpp
  source/frequency_response_window.cpp
  source/app_state.hpp
  source/audio_data.hpp
  source/application.hpp
  source/audio_window.hpp
  source/azimuth_window.hpp
  source/thd_window.hpp
  source/frequency_response_window.hpp
  ${turntable_tools_SOURCE}
  ${imgui_SOURCE}
  ${third_party_SOURCE}
)

add_executable(TurntableTools::exe ALIAS TurntableTools_exe)
target_compile_definitions(TurntableTools_exe
  PRIVATE IMGUI_IMPL_OPENGL_LOADER_GLAD
)

set_property(TARGET TurntableTools_exe PROPERTY OUTPUT_NAME TurntableTools)

target_compile_features(TurntableTools_exe PRIVATE cxx_std_20)

target_link_libraries(TurntableTools_exe
  PRIVATE
  OpenGL::OpenGL
  glfw
)

target_include_directories(TurntableTools_exe SYSTEM PRIVATE ${imgui_SOURCE_DIR} ${implot_SOURCE_DIR} ${pocketfft_SOURCE_DIR})

target_compile_definitions(TurntableTools_exe PRIVATE MA_NO_MP3)

# add_subdirectory("${PROJECT_SOURCE_DIR}/test")

