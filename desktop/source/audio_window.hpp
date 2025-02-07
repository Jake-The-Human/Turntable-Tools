#pragma once

#include <filesystem>
#include <map>

#include <implot.h>

#include "app_state.hpp"
#include "audio_data.hpp"

struct AudioWindow
{
  auto renderUI() -> void;
  auto renderGraphs(int item_graph_idx,
                    AudioData& audio_data,
                    TimeSelection& selection) -> void;

  std::map<std::filesystem::path, bool> open_tabs;
  std::filesystem::path active_file;
};
