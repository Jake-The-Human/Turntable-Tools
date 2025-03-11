include(FetchContent)

find_package(OpenGL REQUIRED)
find_package(glfw3 CONFIG REQUIRED)
# find_package(glad CONFIG REQUIRED)

FetchContent_Declare(
  implot
  GIT_REPOSITORY https://github.com/epezent/implot.git
  GIT_TAG master
  GIT_SHALLOW TRUE
  EXCLUDE_FROM_ALL
)

FetchContent_Declare(
  imgui
  GIT_REPOSITORY https://github.com/ocornut/imgui.git
  GIT_TAG v1.91.8
  GIT_SHALLOW TRUE
  EXCLUDE_FROM_ALL
)

FetchContent_Declare(
  PocketFFT
  GIT_REPOSITORY https://gitlab.mpcdf.mpg.de/mtr/pocketfft.git
  GIT_TAG origin/cpp
  GIT_SHALLOW TRUE
  EXCLUDE_FROM_ALL
)

FetchContent_Declare(
  argparse
  GIT_REPOSITORY https://github.com/p-ranav/argparse.git
  GIT_TAG v3.1
  GIT_SHALLOW TRUE
  EXCLUDE_FROM_ALL
)

FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.7.1
  GIT_SHALLOW TRUE
  EXCLUDE_FROM_ALL
)

# Disable tests after fetching
# set(ARGPARSE_BUILD_TESTS OFF CACHE BOOL "Disable building tests for argparse" FORCE)
# set(ARGPARSE_BUILD_SAMPLES OFF CACHE BOOL "Disable building samples for argparse" FORCE)

FetchContent_MakeAvailable(
  implot
  imgui
  PocketFFT
  Catch2
)

set(imgui_SOURCE
  ${implot_SOURCE_DIR}/implot.cpp
  ${implot_SOURCE_DIR}/implot_internal.h
  ${implot_SOURCE_DIR}/implot_items.cpp
  ${implot_SOURCE_DIR}/implot_demo.cpp
  ${imgui_SOURCE_DIR}/imgui.cpp
  ${imgui_SOURCE_DIR}/imgui_draw.cpp
  ${imgui_SOURCE_DIR}/imgui_tables.cpp
  ${imgui_SOURCE_DIR}/imgui_widgets.cpp
  ${imgui_SOURCE_DIR}/imgui_demo.cpp
  ${imgui_SOURCE_DIR}/backends/imgui_impl_glfw.cpp
  ${imgui_SOURCE_DIR}/backends/imgui_impl_opengl3.cpp
)
