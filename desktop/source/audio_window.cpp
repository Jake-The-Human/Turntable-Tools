#include <array>
#include <cstdio>
#include <filesystem>

#include "audio_window.hpp"

#include <imgui.h>
#include <implot.h>

auto AudioWindow::renderUI(AppData& app_data, AudioData& audio_data) -> void
{
  ImGui::Begin("Audio Information");
  ImGui::Text("Drag and drop WAV files here!");

  // Create tabs
  static ImGuiTabBarFlags tab_bar_flags = ImGuiTabBarFlags_None
      | ImGuiTabBarFlags_Reorderable | ImGuiTabBarFlags_AutoSelectNewTabs;
  if (ImGui::BeginTabBar("AudioFilesTabBar", tab_bar_flags)) {
    for (auto& current_tab : open_tabs) {
      const auto& current_file = current_tab.first.filename();
      if (ImGui::BeginTabItem(current_file.c_str(),
                              &current_tab.second,
                              ImGuiTabItemFlags_None))
      {
        if (active_file != current_tab.first) {
          active_file = current_tab.first;

          if (!audio_data.update(current_tab.first)) {
            ImGui::Text("File failed to load: %s", current_tab.first.c_str());
            fprintf(
                stderr, "File failed to load: %s\n", current_tab.first.c_str());
          } else {
            app_data.time_selection.start = 0;
            app_data.time_selection.end = audio_data.lenInSeconds();
          }
        }

        renderGraphs(app_data, audio_data);

        ImGui::EndTabItem();
      }
    }
    ImGui::EndTabBar();

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

auto AudioWindow::renderGraphs(AppData& app_data, AudioData& audio_data) -> void
{
  if (audio_data.fileLoaded()) {
    ImGui::Text("File: %s", audio_data.file_path.c_str());
    ImGui::Text("Channels: %d", audio_data.channels);
    ImGui::Text("Sample Rate: %uHz", audio_data.sample_rate);
    ImGui::Text("Length: %llus", audio_data.lenInSeconds());
    ImGui::Separator();

    static int item_selected_idx = 0;
    static const std::array<const char*, 3> items = {
        "Stereo", "Split Channels", "Spectrogram"};
    if (ImGui::BeginCombo("Graph", items[item_selected_idx])) {
      for (int n = 0; n < items.size(); n++) {
        const bool is_selected = (item_selected_idx == n);
        if (ImGui::Selectable(items[n], is_selected))
          item_selected_idx = n;

        // Set the initial focus when opening the combo (scrolling +
        // keyboard navigation focus)
        if (is_selected)
          ImGui::SetItemDefaultFocus();
      }
      ImGui::EndCombo();
    }

    ImGui::SameLine();

    app_data.update_data = ImGui::Button("Refresh Measurements");

    ImGui::SameLine();
    ImGui::Text("Selection: %.2fs",
                app_data.time_selection.end - app_data.time_selection.start);

    static const auto blue = ImVec4(0.25, 0.25, 0.9, 1);
    static const auto red = ImVec4(0.9, 0.25, 0.25, 1);

    static const int decimationFactor = 512;
    int reducedSize = audio_data.total_PCM_frame_count / decimationFactor;

    std::vector<float> reducedTime(reducedSize);
    std::vector<float> reducedLeft(reducedSize);
    std::vector<float> reducedRight(reducedSize);

    for (int i = 0; i < reducedSize; i++) {
      int idx = i * decimationFactor;
      reducedTime[i] = static_cast<float>(idx) / audio_data.sample_rate;
      reducedLeft[i] = audio_data.left_channel[idx];
      reducedRight[i] = audio_data.right_channel[idx];
    }

    static bool start_line_dragging = false;
    static bool end_line_dragging = false;

    double start_graph_marker = app_data.time_selection.start;
    double end_graph_marker = app_data.time_selection.end;

    if (item_selected_idx == 0) {
      if (ImPlot::BeginPlot("Stereo Audio Waveform")) {
        ImPlot::SetupAxes("Time (s)", "Amplitude");
        ImPlot::SetNextLineStyle(blue, 1.5f);
        ImPlot::PlotLine(
            "Left", reducedTime.data(), reducedLeft.data(), reducedSize);
        ImPlot::SetNextLineStyle(red, 1.5f);
        ImPlot::PlotLine(
            "Right", reducedTime.data(), reducedRight.data(), reducedSize);
        ImPlot::DragLineX(0, &start_graph_marker, ImVec4(1, 1, 1, 1), 1);
        ImPlot::DragLineX(1, &end_graph_marker, ImVec4(1, 1, 1, 1), 1);
        ImPlot::EndPlot();
      }
    } else if (item_selected_idx == 1) {
      static const auto subplot_flag = ImPlotSubplotFlags_LinkRows
          | ImPlotSubplotFlags_LinkAllY | ImPlotSubplotFlags_LinkAllX;
      if (ImPlot::BeginSubplots(
              "##AxisLinking", 2, 1, ImVec2(-1, -1), subplot_flag))
      {
        if (ImPlot::BeginPlot("Left Channel")) {
          ImPlot::SetupAxesLimits(0, audio_data.lenInSeconds(), -1, 1);
          ImPlot::SetupAxes("Time (s)", "Amplitude");
          ImPlot::SetNextLineStyle(blue, 1.5f);
          ImPlot::PlotLine("Left Channel",
                           reducedTime.data(),
                           reducedLeft.data(),
                           reducedSize);
          ImPlot::DragLineX(0, &start_graph_marker, ImVec4(1, 1, 1, 1), 1);
          ImPlot::DragLineX(1, &end_graph_marker, ImVec4(1, 1, 1, 1), 1);
          ImPlot::EndPlot();
        }
        if (ImPlot::BeginPlot("Right Channel")) {
          ImPlot::SetupAxesLimits(0, audio_data.lenInSeconds(), -1, 1);
          ImPlot::SetupAxes("Time (s)", "Amplitude");
          ImPlot::SetNextLineStyle(red, 1.5f);
          ImPlot::PlotLine("Right Channel",
                           reducedTime.data(),
                           reducedRight.data(),
                           reducedSize);
          ImPlot::DragLineX(0, &start_graph_marker, ImVec4(1, 1, 1, 1), 1);
          ImPlot::DragLineX(1, &end_graph_marker, ImVec4(1, 1, 1, 1), 1);
          ImPlot::EndPlot();
        }
        ImPlot::EndSubplots();
      }
    } else {
      ImGui::Text("Coming soon!");
    }

    bool bad_selection = start_graph_marker >= end_graph_marker
        || end_graph_marker <= start_graph_marker;
    if (!bad_selection) {
      app_data.time_selection = {start_graph_marker, end_graph_marker};
    }
  }
}
