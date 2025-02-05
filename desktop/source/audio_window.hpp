#pragma once

#include <filesystem>
#include <map>

#include <implot.h>

#include "app_state.hpp"
#include "audio_data.hpp"

struct AudioWindow
{
  auto renderUI(AppData& app_data, AudioData& audio_data) -> void;
  auto renderGraphs(AppData& app_data, AudioData& audio_data) -> void;

  std::map<std::filesystem::path, bool> open_tabs;
  std::filesystem::path active_file;
};
