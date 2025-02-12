#pragma once

#include <future>
#include <utility>

#include "imgui.h"

#include "audio_data.hpp"
#include "tools/azimuth.hpp"
#include "tools/frequency_response.hpp"

struct TimeSelection
{
  double start = 0.0;
  double end = 0.0;
};

class AppStateSingleton
{
public:
  ~AppStateSingleton() = default;

  static AppStateSingleton& getInstance() { return *instance; }

  static void newInstance()
  {
    if (instance == nullptr) {
      instance = new AppStateSingleton();
    }
  }

  static void deleteInstance()
  {
    if (instance != nullptr) {
      delete instance;
    }
  }

  std::vector<std::string>* dragged_and_dropped_files_ptr;

  // Style
  float global_scale = 1.0f;

  // GuiState
  bool azimuth_window = false;
  bool thd_window = false;
  bool freq_response = false;

  // AppData
  bool update_data = false;
  TimeSelection time_selection;
  AudioData current_audio;
  std::future<std::pair<FrequencyResponseResults, FrequencyResponseResults>>
      freq_response_results;
  std::future<azimuth::Results> azimuth_results;
  std::future<std::pair<float, float>> thd_results;
  std::atomic_bool cancel_analysis = false;
  std::atomic_bool finished_azimuth = false;
  std::atomic_bool finished_thd = false;
  std::atomic_bool finished_freq_response = false;

private:
  static AppStateSingleton* instance;

  void loadStyle() { ImGuiStyle& my_style = ImGui::GetStyle(); }
  void saveStyle() { ImGuiStyle& my_style = ImGui::GetStyle(); }

  AppStateSingleton() = default;

  AppStateSingleton(const AppStateSingleton&) = delete;
  AppStateSingleton(AppStateSingleton&&) = delete;

  AppStateSingleton& operator=(const AppStateSingleton&) = delete;
  AppStateSingleton& operator=(AppStateSingleton&&) = delete;
};
