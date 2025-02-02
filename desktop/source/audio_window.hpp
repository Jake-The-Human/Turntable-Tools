#pragma once

#include <cstddef>
#include <filesystem>
#include <map>
#include <string>
#include <vector>

#include <dr_wav.h>
#include <implot.h>

struct AudioWindow
{
  ~AudioWindow();
  AudioWindow(std::vector<std::string>* dragged_and_dropped_files);
  AudioWindow(const AudioWindow&) = default;
  AudioWindow(AudioWindow&&) = default;

  AudioWindow& operator=(const AudioWindow&) = default;
  AudioWindow& operator=(AudioWindow&&) = default;

  void renderUI();

  std::vector<std::string>* dragged_and_dropped_files_ptr;
  std::map<std::filesystem::path, bool> open_tabs;
  std::filesystem::path active_file;

  // implot
  ImPlotContext* imPlot_context = nullptr;

  // audio data
  std::vector<float> time;
  std::vector<float> left_channel;
  std::vector<float> right_channel;

  // dr_wav
  bool split_graph_channels = false;
  drwav_uint32 channels;
  drwav_uint32 sampleRate;
  drwav_uint64 totalPCMFrameCount;
  float* pSampleData = nullptr;
  size_t reducedSize = 0;
};
