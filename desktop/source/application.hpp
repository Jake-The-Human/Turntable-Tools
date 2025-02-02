#pragma once

#include <string>
#include <vector>

#include "audio_window.hpp"
#include "imgui.h"

struct MyApp
{
  ~MyApp() = default;
  MyApp(std::vector<std::string>* dragged_and_dropped_files)
      : audio_window(dragged_and_dropped_files)
  {
  }
  MyApp(const MyApp&) = default;
  MyApp(MyApp&&) = default;

  MyApp& operator=(const MyApp&) = default;
  MyApp& operator=(MyApp&&) = default;

  bool renderUI(const ImGuiIO& io);

  struct GuiState
  {
    bool azimuth_window = false;
    bool thd_window = false;
    bool freq_response = false;
  } gui_state;

  AudioWindow audio_window;
};
