project(TurntableToolsTests LANGUAGES CXX)

# Enable testing
enable_testing()

add_executable(TurntableTools_test
    source/TurntableTools_test.cpp
    source/frequency_response.cpp
    source/tracking_ability_test.cpp
)

# Link Catch2 to the test executable
target_link_libraries(TurntableTools_test PRIVATE Catch2::Catch2WithMain TurntableTools_lib)

# Enable C++20 (or required standard) for the tests
target_compile_features(TurntableTools_test PRIVATE cxx_std_20)

# target_include_directories(TurntableTools_test PRIVATE ${Catch2_SOURCE_DIR}/src)

# ---- End-of-file commands ----
# list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)
include(CTest)
include(Catch)
catch_discover_tests(TurntableTools_test)