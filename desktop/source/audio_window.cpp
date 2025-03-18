#include <array>
#include <cstdio>
#include <filesystem>

#include "audio_window.hpp"

#include "app_state.hpp"
#include "imgui.h"
#include "implot.h"
#include "message_catalog.hpp"

struct DownSampler
{
  int start;
  int end;
  int size;
  int stride;
};

static DownSampler downsampler(int data_size,
                               int sampling_rate,
                               int t_min,
                               int t_max)
{
  static const int downsample_factor = data_size / 2;
  int downsample = static_cast<int>(
      (ImPlot::GetPlotLimits().X.Size() * sampling_rate) / downsample_factor
      + 1);
  int start =
      static_cast<int>(ImPlot::GetPlotLimits().X.Min - t_min) * sampling_rate;
  start = start < 0 ? 0 : start > data_size - 1 ? data_size - 1 : start;
  int end =
      (static_cast<int>(ImPlot::GetPlotLimits().X.Max - t_min) * sampling_rate)
      + downsample_factor;
  end = end < 0 ? 0 : end > data_size - 1 ? data_size - 1 : end;
  int size = (end - start) / downsample;

  return {.start = start, .end = end, .size = size, .stride = downsample};
}

void AudioWindow::renderUI()
{
  auto& app_state = AppStateSingleton::getInstance();
  auto& audio_data = app_state.current_audio;
  const auto& messages = MessageCatalog::getInstance();

  ImGui::Begin("Audio Information");
  ImGui::Text("Drag and drop WAV files here!");
  ImGui::Spacing();
  ImGui::BeginChild("AUDIO_OVERVIEW", {-1, -1});
  {
    // Create tabs
    static const ImGuiTabBarFlags tab_bar_flags = ImGuiTabBarFlags_None
        | ImGuiTabBarFlags_Reorderable | ImGuiTabBarFlags_AutoSelectNewTabs;
    if (ImGui::BeginTabBar("AudioFilesTabBar", tab_bar_flags)) {
      for (auto& current_tab : open_tabs) {
        const auto& current_file = current_tab.first.filename().string();
        if (ImGui::BeginTabItem(current_file.c_str(),
                                &current_tab.second,
                                ImGuiTabItemFlags_None))
        {
          if (active_file != current_tab.first) {
            active_file = current_tab.first;

            if (!audio_data.update(current_tab.first)) {
              ImGui::Text("File failed to load: %s", current_tab.first.c_str());
            } else {
              app_state.time_selection.start = 0;
              app_state.time_selection.end = audio_data.lenInSeconds();
            }
          }

          if (audio_data.fileLoaded()) {
            ImGui::Text("File: %s", audio_data.file_path.c_str());
            ImGui::Text("Channels: %d", audio_data.channels);
            ImGui::Text("Sample Rate: %uHz", audio_data.sample_rate);
            // ImGui::Text("Length: %llus", audio_data.lenInSeconds());
            ImGui::Separator();

            static int item_graph_idx = 0;
            static const std::array<const char*, 2> graphs = {"Stereo",
                                                              "Split Channels"};
            if (ImGui::BeginCombo("Graph", graphs[item_graph_idx])) {
              for (int n = 0; n < graphs.size(); n++) {
                const bool is_selected = (item_graph_idx == n);
                if (ImGui::Selectable(graphs[n], is_selected))
                  item_graph_idx = n;

                // Set the initial focus when opening the combo (scrolling +
                // keyboard navigation focus)
                if (is_selected)
                  ImGui::SetItemDefaultFocus();
              }
              ImGui::EndCombo();
            }

            ImGui::SameLine();

            if (ImGui::Button("Refresh Measurements")) {
              app_state.update_data = true;
              ImGui::OpenPopup("Analyzing Audio");
            } else {
              app_state.update_data = false;
            }
            ImGui::SameLine();
            ImGui::Text(
                "Selection: %.2fs",
                app_state.time_selection.end - app_state.time_selection.start);
            renderGraphs(item_graph_idx, audio_data, app_state.time_selection);

            if (ImGui::BeginPopupModal("Analyzing Audio")) {
              ImGui::ProgressBar(-1.0f * (float)ImGui::GetTime(),
                                 ImVec2(0.0f, 0.0f),
                                 "Analyzing...");

              ImGui::SameLine();
              if (ImGui::Button("Cancel")) {
                app_state.cancel_analysis = true;
                ImGui::CloseCurrentPopup();
              }

              if (app_state.finished_azimuth && app_state.finished_thd
                  && app_state.finished_freq_response)
              {
                app_state.finished_azimuth = false;
                app_state.finished_thd = false;
                app_state.finished_freq_response = false;
                ImGui::CloseCurrentPopup();
              }
              ImGui::EndPopup();
            }
          }

          ImGui::EndTabItem();
        }
      }
      ImGui::EndTabBar();
    }
    ImGui::EndChild();

    // Delete any closed tabs
    std::vector<std::map<std::filesystem::path, bool>::iterator> to_remove;
    to_remove.reserve(open_tabs.size());
    for (auto it = open_tabs.begin(); it != open_tabs.end(); ++it) {
      if (!it->second) {
        to_remove.push_back(it);
      }
    }

    for (auto it : to_remove) {
      open_tabs.erase(it);
    }
  }

  ImGui::End();
}

void AudioWindow::renderGraphs(int item_graph_idx,
                               AudioData& audio_data,
                               TimeSelection& selection)
{
  const auto& messages = MessageCatalog::getInstance();

  static const auto blue = ImVec4(0.25, 0.25, 0.9, 1);
  static const auto red = ImVec4(0.9, 0.25, 0.25, 1);

  std::vector<float> time_axis(audio_data.total_PCM_frame_count);
  for (int i = 0; i < time_axis.size(); i++) {
    time_axis[i] = static_cast<float>(i) / audio_data.sample_rate;
  }

  static bool start_line_dragging = false;
  static bool end_line_dragging = false;

  double start_graph_marker = selection.start;
  double end_graph_marker = selection.end;

  if (item_graph_idx == 0) {
    if (ImPlot::BeginPlot("Stereo Audio Waveform")) {
      ImPlot::SetupAxes("Time (s)", "Amplitude");
      ImPlot::SetupAxesLimits(0.0, audio_data.lenInSeconds(), -1.f, 1.f);
      ImPlot::SetNextLineStyle(blue);
      auto downsample_data = downsampler(audio_data.total_PCM_frame_count,
                                         audio_data.sample_rate,
                                         0,
                                         audio_data.lenInSeconds());
      ImPlot::PlotLine("Left",
                       &time_axis[downsample_data.start],
                       &audio_data.left_channel[downsample_data.start],
                       downsample_data.size,
                       0,
                       0,
                       sizeof(float) * downsample_data.stride);
      ImPlot::SetNextLineStyle(red);
      ImPlot::PlotLine("Right",
                       &time_axis[downsample_data.start],
                       &audio_data.right_channel[downsample_data.start],
                       downsample_data.size,
                       0,
                       0,
                       sizeof(float) * downsample_data.stride);
      ImPlot::DragLineX(0, &start_graph_marker, ImVec4(1, 1, 1, 1), 1);
      ImPlot::DragLineX(1, &end_graph_marker, ImVec4(1, 1, 1, 1), 1);
      ImPlot::EndPlot();
    }
  } else if (item_graph_idx == 1) {
    static const auto subplot_flag = ImPlotSubplotFlags_LinkRows
        | ImPlotSubplotFlags_LinkAllY | ImPlotSubplotFlags_LinkAllX;
    if (ImPlot::BeginSubplots(
            "##AxisLinking", 2, 1, ImVec2(-1, -1), subplot_flag))
    {
      if (ImPlot::BeginPlot("Left Channel")) {
        ImPlot::SetupAxes("Time (s)", "Amplitude");
        ImPlot::SetupAxesLimits(0, audio_data.lenInSeconds(), -1.f, 1.f);
        auto downsample_data = downsampler(audio_data.total_PCM_frame_count,
                                           audio_data.sample_rate,
                                           0,
                                           audio_data.lenInSeconds());
        ImPlot::SetNextLineStyle(blue);
        ImPlot::PlotLine("Left Channel",
                         &time_axis[downsample_data.start],
                         &audio_data.left_channel[downsample_data.start],
                         downsample_data.size,
                         0,
                         0,
                         sizeof(float) * downsample_data.stride);
        ImPlot::DragLineX(0, &start_graph_marker, ImVec4(1, 1, 1, 1), 1);
        ImPlot::DragLineX(1, &end_graph_marker, ImVec4(1, 1, 1, 1), 1);
        ImPlot::EndPlot();
      }
      if (ImPlot::BeginPlot("Right Channel")) {
        ImPlot::SetupAxes("Time (s)", "Amplitude");
        ImPlot::SetupAxesLimits(0, audio_data.lenInSeconds(), -1.f, 1.f);
        auto downsample_data = downsampler(audio_data.total_PCM_frame_count,
                                           audio_data.sample_rate,
                                           0,
                                           audio_data.lenInSeconds());
        ImPlot::SetNextLineStyle(red);
        ImPlot::PlotLine("Right Channel",
                         &time_axis[downsample_data.start],
                         &audio_data.right_channel[downsample_data.start],
                         downsample_data.size,
                         0,
                         0,
                         sizeof(float) * downsample_data.stride);
        ImPlot::DragLineX(0, &start_graph_marker, ImVec4(1, 1, 1, 1), 1);
        ImPlot::DragLineX(1, &end_graph_marker, ImVec4(1, 1, 1, 1), 1);
        ImPlot::EndPlot();
      }
      ImPlot::EndSubplots();
    }
  }

  start_graph_marker = std::max(start_graph_marker, 0.0);
  end_graph_marker =
      std::min(end_graph_marker, (double)audio_data.lenInSeconds());
  bool bad_selection = start_graph_marker >= end_graph_marker
      || end_graph_marker <= start_graph_marker;
  if (!bad_selection) {
    selection = {start_graph_marker, end_graph_marker};
  }
}
