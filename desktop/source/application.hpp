#pragma once

#include <string>
#include <vector>

#include <imgui.h>

#include "app_state.hpp"
#include "audio_window.hpp"
#include "azimuth_window.hpp"
#include "frequency_response_window.hpp"
#include "thd_window.hpp"

constexpr auto NUMBER_OF_TESTS = 3;

struct MyApp
{
  ~MyApp() = default;
  MyApp(std::vector<std::string>* dragged_and_dropped_files)
      : dragged_and_dropped_files_ptr(dragged_and_dropped_files)
  {
  }
  MyApp(const MyApp&) = delete;
  MyApp(MyApp&&) = delete;

  MyApp& operator=(const MyApp&) = delete;
  MyApp& operator=(MyApp&&) = delete;

  bool renderUI(const ImGuiIO& io);
  void updateState();

  std::vector<std::string>* dragged_and_dropped_files_ptr;
  AudioWindow audio_window;
  AzimuthWindow azimuth_window;
  ThdWindow thd_window;
  FrequencyResponseWindow freq_window;

  GuiState gui_state;
  AppData app_data;
  bool analyzing_modal = false;
};
