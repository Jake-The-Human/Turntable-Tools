#pragma once

#include <future>

#include "tools/azimuth.hpp"

struct AzimuthWindow
{
  void renderUI(bool& window_state,
                std::future<azimuth::Results>& azimuth_results,
                bool file_loaded);
  int test_frequency = 1000;
  azimuth::Results results;
};
