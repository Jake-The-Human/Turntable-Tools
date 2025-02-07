#include <cmath>
#include <cstdio>
#include <utility>

#include "application.hpp"

#include <imgui.h>
#include <implot.h>

#include "audio_data.hpp"
#include "toolbar.hpp"
#include "tools/azimuth.hpp"
#include "tools/frequency_response.hpp"
#include "tools/moving_avg.hpp"
#include "tools/thd.hpp"

bool MyApp::renderUI(const ImGuiIO& io)
{
  // Handle drag and drop and an update the audio window tabs.
  auto& open_tabs = audio_window.open_tabs;
  if (!dragged_and_dropped_files_ptr->empty()) {
    for (const auto& file : *dragged_and_dropped_files_ptr) {
      auto file_path = std::filesystem::path(file);
      if (file_path.extension() == ".wav"
          && open_tabs.find(file_path) == open_tabs.end())
      {
        open_tabs.insert({file_path, true});
      }
    }
    dragged_and_dropped_files_ptr->clear();
  }

  bool exit_app = MainMenuBar(gui_state);

  audio_window.renderUI(app_data, app_data.current_audio);
  bool file_loaded = app_data.current_audio.fileLoaded();

  if (gui_state.azimuth_window) {
    azimuth_window.renderUI(
        gui_state.azimuth_window, app_data.azimuth_results, file_loaded);
  }

  if (gui_state.thd_window) {
    thd_window.renderUI(
        gui_state.thd_window, app_data.thd_results, file_loaded);
  }

  if (gui_state.freq_response) {
    freq_window.renderUI(
        gui_state.freq_response, app_data.freq_response_results, file_loaded);
  }

  // ImPlot::ShowDemoWindow();
  // ImGui::ShowDemoWindow();
  return exit_app;
}

void MyApp::updateState()
{
  if (app_data.current_audio.fileLoaded() && app_data.update_data) {
    app_data.azimuth_results = std::async(
        std::launch::async,
        [&]
        {
          app_data.finished_azimuth = false;

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
          auto start_time = app_data.time_selection.start;
          auto end_time = app_data.time_selection.end;

          auto left_channel = app_data.current_audio.getSectionOfData(
              AudioData::Channel::LEFT, start_time, end_time);
          auto right_channel = app_data.current_audio.getSectionOfData(
              AudioData::Channel::RIGHT, start_time, end_time);

          for (int i = 0; i < left_channel.size() - chunk; i += chunk) {
            results = azimuth_avg.update(
                azimuth::update({&left_channel[i], &left_channel[i + chunk]},
                                {&right_channel[i], &right_channel[i + chunk]},
                                test_freq,
                                app_data.current_audio.sample_rate));
          }
          app_data.finished_azimuth = true;
          return results;
        });
    app_data.thd_results = std::async(
        std::launch::async,
        [&]
        {
          app_data.finished_thd = false;

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
          auto start_time = app_data.time_selection.start;
          auto end_time = app_data.time_selection.end;

          auto left_channel = app_data.current_audio.getSectionOfData(
              AudioData::Channel::LEFT, start_time, end_time);
          auto right_channel = app_data.current_audio.getSectionOfData(
              AudioData::Channel::RIGHT, start_time, end_time);

          for (int i = 0; i < left_channel.size() - chunk; i += chunk) {
            results = thd_avg.update(
                {thd::calculate({&left_channel[i], &left_channel[i + chunk]}),
                 thd::calculate(
                     {&right_channel[i], &right_channel[i + chunk]})});
          }
          app_data.finished_thd = true;
          return results;
        });

    app_data.freq_response_results = std::async(
        std::launch::async,
        [&]
        {
          app_data.finished_freq_response = false;
          auto chunk = AudioData::MIN_SIZE;
          auto start_time = app_data.time_selection.start;
          auto end_time = app_data.time_selection.end;

          auto left_channel = app_data.current_audio.getSectionOfData(
              AudioData::Channel::LEFT, start_time, end_time);
          auto right_channel = app_data.current_audio.getSectionOfData(
              AudioData::Channel::RIGHT, start_time, end_time);
          auto sampling_rate = app_data.current_audio.sample_rate;

          FrequencyResponse fr_l;
          FrequencyResponse fr_r;

          for (int i = 0; i < left_channel.size() - chunk; i += chunk) {
            fr_l.update({&left_channel[i], &left_channel[i + chunk]},
                        sampling_rate);
            fr_r.update({&right_channel[i], &right_channel[i + chunk]},
                        sampling_rate);
          }
          app_data.finished_freq_response = true;
          return std::make_pair(fr_l.frequency_response_map,
                                fr_r.frequency_response_map);
        });
  }
}
