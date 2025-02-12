#pragma once

#include <future>

struct ThdWindow
{
  void renderUI(bool& window_state,
                std::future<std::pair<float, float>>& thd_results,
                bool file_loaded);
  std::pair<float, float> results;
};
