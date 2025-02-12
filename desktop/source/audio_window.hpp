#pragma once

#include <filesystem>
#include <map>

#include "app_state.hpp"
#include "audio_data.hpp"

struct AudioWindow
{
  void renderUI();
  void renderGraphs(int item_graph_idx,
                    AudioData& audio_data,
                    TimeSelection& selection);

  std::map<std::filesystem::path, bool> open_tabs;
  std::filesystem::path active_file;
};
