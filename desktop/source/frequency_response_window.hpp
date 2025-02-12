#pragma once

#include <future>
#include <utility>
#include <vector>

#include "tools/frequency_response.hpp"

struct FrequencyResponseWindow
{
  void renderUI(bool& window_state,
                std::future<std::pair<FrequencyResponseResults,
                                      FrequencyResponseResults>>& fr_results,
                bool file_loaded);

  std::vector<float> freq_left;
  std::vector<float> magnitude_left;
  std::vector<float> phase_left;

  std::vector<float> freq_right;
  std::vector<float> magnitude_right;
  std::vector<float> phase_right;
};
