#pragma once

#include <future>
#include <utility>

#include "audio_data.hpp"
#include "tools/azimuth.hpp"
#include "tools/frequency_response.hpp"

struct GuiState
{
  bool azimuth_window = false;
  bool thd_window = false;
  bool freq_response = false;
};

struct AppData
{
  bool update_data = false;
  struct
  {
    double start = 0;
    double end = 0;
  } time_selection;
  AudioData current_audio;
  std::future<std::pair<FrequencyResponseResults, FrequencyResponseResults>>
      freq_response_results;
  std::future<azimuth::Results> azimuth_results;
  std::future<std::pair<float, float>> thd_results;
};
