#pragma once

#include <filesystem>
#include <span>
#include <vector>

#include "dr_wav.h"

struct AudioData
{
  enum class Channel : int
  {
    LEFT = 0,
    RIGHT = 1,
  };
  auto update(const std::filesystem::path& wav_path) -> bool;

  auto getSectionOfData(Channel channel, float start_time, float end_time)
      -> std::span<const float>;

  auto lenInSeconds() const { return total_PCM_frame_count / sample_rate; }
  auto fileLoaded() const { return !time.empty(); }

  static const size_t MIN_SIZE = 1024;
  std::filesystem::path file_path;
  drwav_uint32 channels;
  drwav_uint32 sample_rate;
  drwav_uint64 total_PCM_frame_count;
  std::vector<float> time;
  std::vector<float> left_channel;
  std::vector<float> right_channel;
};
