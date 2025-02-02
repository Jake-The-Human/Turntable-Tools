#include <cstdio>
#include <filesystem>

#include "audio_window.hpp"

#include <imgui.h>
#include <implot.h>

AudioWindow::~AudioWindow()
{
  if (pSampleData != nullptr) {
    drwav_free(pSampleData, nullptr);
    pSampleData = nullptr;
  }
}

AudioWindow::AudioWindow(std::vector<std::string>* dragged_and_dropped_files)
    : dragged_and_dropped_files_ptr(dragged_and_dropped_files)
{
}

void AudioWindow::renderUI()
{
  ImGui::Begin("Audio Information");
  ImGui::Text("Drag and drop WAV files here!");

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
        ImGui::Text("Current File: %s", current_file.c_str());
        ImGui::Separator();

        if (active_file != current_tab.first) {
          active_file = current_tab.first;

          if (pSampleData != nullptr) {
            drwav_free(pSampleData, nullptr);
            pSampleData = nullptr;
          }

          pSampleData =
              drwav_open_file_and_read_pcm_frames_f32(current_file.c_str(),
                                                      &channels,
                                                      &sampleRate,
                                                      &totalPCMFrameCount,
                                                      nullptr);
          if (pSampleData == nullptr) {
            ImGui::Text("File failed to load: %s", current_file.c_str());
            fprintf(stderr, "File failed to load: %s\n", current_file.c_str());
          } else {
            // get data for graph
            time.resize(totalPCMFrameCount);
            left_channel.resize(totalPCMFrameCount);
            right_channel.resize(totalPCMFrameCount);
            for (size_t i = 0; i < totalPCMFrameCount; ++i) {
              time[i] = static_cast<float>(i) / static_cast<float>(sampleRate);
              left_channel[i] = pSampleData[i * channels];
              right_channel[i] =
                  (channels > 1) ? pSampleData[i * channels + 1] : 0.0f;
            }
          }
        }

        if (pSampleData != nullptr) {
          ImGui::Text("Channels: %d", channels);
          ImGui::Text("Sample Rate: %uHz", sampleRate);
          ImGui::Text("Length: %llus", totalPCMFrameCount / sampleRate);
          ImGui::Separator();

          ImGui::Checkbox("Split Channels", &split_graph_channels);

          static const auto white = ImVec4(1, 1, 1, 1);
          static const auto red = ImVec4(1, 0, 0, 1);

          static const int decimationFactor = 512;
          int reducedSize = totalPCMFrameCount / decimationFactor;

          std::vector<float> reducedTime(reducedSize);
          std::vector<float> reducedLeft(reducedSize);
          std::vector<float> reducedRight(reducedSize);

          for (int i = 0; i < reducedSize; i++) {
            int idx = i * decimationFactor;
            reducedTime[i] = static_cast<float>(idx) / sampleRate;
            reducedLeft[i] = left_channel[idx];
            reducedRight[i] = right_channel[idx];
          }

          static const auto y_min = -1.1F;
          static const auto y_max = 1.1F;

          if (!split_graph_channels) {
            if (ImPlot::BeginPlot("Stereo Audio Waveform",
                                  ImVec2(-1, 300),
                                  ImPlotFlags_NoChild))
            {
              float audioLengthSec = static_cast<float>(totalPCMFrameCount)
                  / static_cast<float>(sampleRate);
              //   ImPlot::SetupAxisLimits(
              //       ImAxis_X1, 0, audioLengthSec, ImGuiCond_Always);
              //   ImPlot::SetupAxisLimits(
              //       ImAxis_Y1, y_min, y_max, ImGuiCond_Always);
              ImPlot::SetupAxes("Time (s)", "Amplitude");

              ImPlot::SetNextLineStyle(white, 1.5f);
              ImPlot::PlotLine(
                  "Left", reducedTime.data(), reducedLeft.data(), reducedSize);

              ImPlot::SetNextLineStyle(red, 1.5f);
              ImPlot::PlotLine("Right",
                               reducedTime.data(),
                               reducedRight.data(),
                               reducedSize);
              ImPlot::EndPlot();
            }
          } else {
            if (ImPlot::BeginPlot("Left Channel Waveform")) {
              float audioLengthSec = static_cast<float>(totalPCMFrameCount)
                  / static_cast<float>(sampleRate);
              //   ImPlot::SetupAxisLimits(
              //       ImAxis_X1, 0, audioLengthSec, ImGuiCond_Always);
              //   ImPlot::SetupAxisLimits(
              //       ImAxis_Y1, y_min, y_max, ImGuiCond_Always);
              ImPlot::SetupAxes("Time (s)", "Amplitude");

              ImPlot::SetNextLineStyle(white, 1.5f);
              ImPlot::PlotLine("Left Channel",
                               reducedTime.data(),
                               reducedLeft.data(),
                               reducedSize);
              ImPlot::EndPlot();
            }
            if (ImPlot::BeginPlot("Right Channel Waveform",
                                  ImVec2(-1, 300),
                                  ImPlotFlags_NoChild))
            {
              float audioLengthSec = static_cast<float>(totalPCMFrameCount)
                  / static_cast<float>(sampleRate);
              //   ImPlot::SetupAxisLimits(
              //       ImAxis_X1, 0, audioLengthSec, ImGuiCond_Always);
              //   ImPlot::SetupAxisLimits(
              //       ImAxis_Y1, y_min, y_max, ImGuiCond_Always);
              ImPlot::SetupAxes("Time (s)", "Amplitude");
              ImPlot::SetNextLineStyle(red, 1.5f);
              ImPlot::PlotLine("Right Channel",
                               reducedTime.data(),
                               reducedRight.data(),
                               reducedSize);

              ImPlot::EndPlot();
            }
          }
        }

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
