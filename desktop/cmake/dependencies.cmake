include(FetchContent)

FetchContent_Declare(
    miniaudio
    GIT_REPOSITORY https://github.com/mackron/miniaudio.git
    GIT_TAG 0.11.21
)

FetchContent_Declare(
    PocketFFT
    GIT_REPOSITORY https://gitlab.mpcdf.mpg.de/mtr/pocketfft.git
    GIT_TAG origin/cpp
)

FetchContent_Declare(
    argparse
    GIT_REPOSITORY https://github.com/p-ranav/argparse.git
    GIT_TAG v3.1
)

FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.7.1
)

# # Disable tests after fetching
# set(ARGPARSE_BUILD_TESTS OFF CACHE BOOL "Disable building tests for argparse" FORCE)
# set(ARGPARSE_BUILD_SAMPLES OFF CACHE BOOL "Disable building samples for argparse" FORCE)

FetchContent_MakeAvailable(miniaudio PocketFFT argparse Catch2)
