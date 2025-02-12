#include <cmath>
#include <cstdio>
#include <utility>

#include "application.hpp"

#include "audio_data.hpp"
#include "imgui.h"
#include "message_catalog.hpp"
#include "tools/azimuth.hpp"
#include "tools/frequency_response.hpp"
#include "tools/moving_avg.hpp"
#include "tools/thd.hpp"

static void handleScalingGui(AppStateSingleton& app_state)
{
  ImGuiIO& io = ImGui::GetIO();
  if (io.KeyCtrl) {
    if (ImGui::IsKeyPressed(ImGuiKey_Equal))
    {  // Ctrl + '=' (which is often 'Ctrl + +')
      io.FontGlobalScale = std::min(io.FontGlobalScale + 0.1f, 2.0f);
    }
    if (ImGui::IsKeyPressed(ImGuiKey_Minus)) {  // Ctrl + '-'
      io.FontGlobalScale = std::max(io.FontGlobalScale - 0.1f, 0.3f);
    }
    if (ImGui::IsKeyPressed(ImGuiKey_0)) {  // Ctrl + '0'
      io.FontGlobalScale = 1.0f;
    }
  }

  if (io.KeyAlt) {
    if (ImGui::IsKeyPressed(ImGuiKey_A)) {
      app_state.azimuth_window = true;
      app_state.thd_window = true;
      app_state.freq_response = true;
    }
    if (ImGui::IsKeyPressed(ImGuiKey_C)) {
      app_state.azimuth_window = false;
      app_state.thd_window = false;
      app_state.freq_response = false;
    }
  }
}

bool MyApp::renderUI()
{
  auto& app_state = AppStateSingleton::getInstance();
  handleScalingGui(app_state);

  // Handle drag and drop and an update the audio window tabs.
  auto& open_tabs = audio_window.open_tabs;
  if (!app_state.dragged_and_dropped_files_ptr->empty()) {
    for (const auto& file : *app_state.dragged_and_dropped_files_ptr) {
      auto file_path = std::filesystem::path(file);
      if (file_path.extension() == ".wav"
          && open_tabs.find(file_path) == open_tabs.end())
      {
        open_tabs.insert({file_path, true});
      }
    }
    app_state.dragged_and_dropped_files_ptr->clear();
  }

  audio_window.renderUI();
  bool file_loaded = app_state.current_audio.fileLoaded();

  if (app_state.azimuth_window) {
    azimuth_window.renderUI(
        app_state.azimuth_window, app_state.azimuth_results, file_loaded);
  }

  if (app_state.thd_window) {
    thd_window.renderUI(
        app_state.thd_window, app_state.thd_results, file_loaded);
  }

  if (app_state.freq_response) {
    freq_window.renderUI(
        app_state.freq_response, app_state.freq_response_results, file_loaded);
  }

  // ImPlot::ShowDemoWindow();
  // ImGui::ShowDemoWindow();
  return MainMenuBar();
}

void MyApp::updateState()
{
  auto& app_state = AppStateSingleton::getInstance();
  if (app_state.current_audio.fileLoaded() && app_state.update_data) {
    app_state.azimuth_results = std::async(
        std::launch::async,
        [&]
        {
          app_state.finished_azimuth = false;

          azimuth::Results results = {};
          MovingAverage<azimuth::Results, MOVING_AVG_SIZE> azimuth_avg;
          azimuth_avg.avg_function =
              [](const std::array<azimuth::Results, MOVING_AVG_SIZE>& input)
              -> azimuth::Results
          {
            azimuth::Results sum = {.crosstalk_signal_1 = 0,
                                    .crosstalk_signal_2 = 0,
                                    .phase_diff = 0};
            for (const auto& data : input) {
              sum.crosstalk_signal_1 += data.crosstalk_signal_1;
              sum.crosstalk_signal_2 += data.crosstalk_signal_2;
              sum.phase_diff += data.phase_diff;
            }

            return {
                .crosstalk_signal_1 = sum.crosstalk_signal_1 / MOVING_AVG_SIZE,
                .crosstalk_signal_2 = sum.crosstalk_signal_2 / MOVING_AVG_SIZE,
                .phase_diff = sum.phase_diff / MOVING_AVG_SIZE};
          };
          auto test_freq = azimuth_window.test_frequency;

          auto chunk = AudioData::MIN_SIZE;
          auto start_time = app_state.time_selection.start;
          auto end_time = app_state.time_selection.end;

          auto left_channel = app_state.current_audio.getSectionOfData(
              AudioData::Channel::LEFT, start_time, end_time);
          auto right_channel = app_state.current_audio.getSectionOfData(
              AudioData::Channel::RIGHT, start_time, end_time);

          for (int i = 0; i < left_channel.size() - chunk; i += chunk) {
            results = azimuth_avg.update(
                azimuth::update({&left_channel[i], &left_channel[i + chunk]},
                                {&right_channel[i], &right_channel[i + chunk]},
                                test_freq,
                                app_state.current_audio.sample_rate));
          }
          app_state.finished_azimuth = true;
          return results;
        });
    app_state.thd_results = std::async(
        std::launch::async,
        [&]
        {
          app_state.finished_thd = false;

          std::pair<float, float> results;
          MovingAverage<std::pair<float, float>, MOVING_AVG_SIZE> thd_avg;
          thd_avg.avg_function =
              [](const std::array<std::pair<float, float>, MOVING_AVG_SIZE>&
                     input) -> std::pair<float, float>
          {
            std::pair<float, float> sum = {0, 0};
            for (const auto data : input) {
              sum.first += data.first;
              sum.second += data.second;
            }
            return {sum.first / MOVING_AVG_SIZE, sum.second / MOVING_AVG_SIZE};
          };

          auto chunk = AudioData::MIN_SIZE;
          auto start_time = app_state.time_selection.start;
          auto end_time = app_state.time_selection.end;

          auto left_channel = app_state.current_audio.getSectionOfData(
              AudioData::Channel::LEFT, start_time, end_time);
          auto right_channel = app_state.current_audio.getSectionOfData(
              AudioData::Channel::RIGHT, start_time, end_time);

          for (int i = 0; i < left_channel.size() - chunk; i += chunk) {
            results = thd_avg.update(
                {thd::calculate({&left_channel[i], &left_channel[i + chunk]}),
                 thd::calculate(
                     {&right_channel[i], &right_channel[i + chunk]})});
          }
          app_state.finished_thd = true;
          return results;
        });

    app_state.freq_response_results = std::async(
        std::launch::async,
        [&]
        {
          app_state.finished_freq_response = false;
          auto chunk = AudioData::MIN_SIZE;
          auto start_time = app_state.time_selection.start;
          auto end_time = app_state.time_selection.end;

          auto left_channel = app_state.current_audio.getSectionOfData(
              AudioData::Channel::LEFT, start_time, end_time);
          auto right_channel = app_state.current_audio.getSectionOfData(
              AudioData::Channel::RIGHT, start_time, end_time);
          auto sampling_rate = app_state.current_audio.sample_rate;

          FrequencyResponse fr_l;
          FrequencyResponse fr_r;

          for (int i = 0; i < left_channel.size() - chunk; i += chunk) {
            fr_l.update({&left_channel[i], &left_channel[i + chunk]},
                        sampling_rate);
            fr_r.update({&right_channel[i], &right_channel[i + chunk]},
                        sampling_rate);
          }
          app_state.finished_freq_response = true;
          return std::make_pair(fr_l.frequency_response_map,
                                fr_r.frequency_response_map);
        });
  }
}

bool MyApp::MainMenuBar()
{
  auto& app_state = AppStateSingleton::getInstance();
  auto& catalog = MessageCatalog::getInstance();
  static bool show_settings = false;
  bool exit_app = false;
  if (ImGui::BeginMainMenuBar()) {
    if (ImGui::BeginMenu(catalog.get_message("FILE"))) {
      // Want to add multi lang support but not sure how to do it.
      // if (ImGui::BeginMenu(catalog.get_message("LANGUAGE"))) {
      //   for (const auto& lang : catalog.get_available_languages()) {
      //     if (ImGui::MenuItem(lang.first.c_str())) {
      //       catalog.set_lang(lang.first);
      //     }
      //   }
      //   ImGui::EndMenu();
      // }
      // ImGui::Separator();
      if (ImGui::MenuItem(catalog.get_message("QUIT"), "Alt+F4")) {
        exit_app = true;
      }
      ImGui::EndMenu();
    }

    if (ImGui::BeginMenu(catalog.get_message("VIEW"))) {
      if (ImGui::MenuItem(catalog.get_message("AZIMUTH"))) {
        app_state.azimuth_window = true;
      }

      if (ImGui::MenuItem(catalog.get_message("THD"))) {
        app_state.thd_window = true;
      }

      if (ImGui::MenuItem(catalog.get_message("FREQUENCY_RESPONSE"))) {
        app_state.freq_response = true;
      }
      ImGui::Separator();
      if (ImGui::MenuItem("Open All", "Alt+A")) {
        app_state.azimuth_window = true;
        app_state.thd_window = true;
        app_state.freq_response = true;
      }

      if (ImGui::MenuItem("Close All", "Alt+C")) {
        app_state.azimuth_window = false;
        app_state.thd_window = false;
        app_state.freq_response = false;
      }
      ImGui::Separator();
      if (ImGui::MenuItem("Scale Up", "Ctrl++")) {
        ImGui::GetIO().FontGlobalScale =
            std::min(ImGui::GetIO().FontGlobalScale + 0.1f, 2.0f);
      }
      if (ImGui::MenuItem("Scale Down", "Ctrl+-")) {
        ImGui::GetIO().FontGlobalScale =
            std::max(ImGui::GetIO().FontGlobalScale - 0.1f, 0.3f);
      }
      if (ImGui::MenuItem("Scale Reset", "Ctrl+0")) {
        ImGui::GetIO().FontGlobalScale = 1.0f;
      }

      ImGui::EndMenu();
    }

    ImGui::EndMainMenuBar();
  }

  ImGui::ShowDemoWindow();
  return exit_app;
}
