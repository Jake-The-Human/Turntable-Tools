#include <algorithm>
#include <bit>
#include <cstdint>

#include "audio_data.hpp"

#include "message_catalog.hpp"

constexpr auto upper_power_of_two(drwav_uint64 v)
{
  return std::bit_ceil(v);
}

auto AudioData::update(const std::filesystem::path& wav_path) -> bool
{
  file_path = wav_path;
  float* pSampleData =
      drwav_open_file_and_read_pcm_frames_f32(file_path.c_str(),
                                              &channels,
                                              &sample_rate,
                                              &total_PCM_frame_count,
                                              nullptr);
  if (pSampleData == nullptr) {
    fprintf(stderr,
            MessageCatalog::getInstance().get_message("FILE_FAILED_TO_LOAD"),
            file_path.c_str());
    channels = 0;
    sample_rate = 0;
    time.clear();
    left_channel.clear();
    right_channel.clear();
    return false;
  } else {
    if (total_PCM_frame_count < MIN_SIZE) {
      return false;
    }
    auto updated_size = upper_power_of_two(total_PCM_frame_count);

    // Pre allocate size to a pow of 2
    time.resize(updated_size);
    left_channel.resize(updated_size);
    right_channel.resize(updated_size);

    // add data
    for (size_t i = 0; i < total_PCM_frame_count; ++i) {
      time[i] = static_cast<float>(i) / sample_rate;
      left_channel[i] = pSampleData[i * channels];
      right_channel[i] = (channels > 1) ? pSampleData[i * channels + 1] : 0.0f;
    }

    // pad the input to always make it a power of 2
    for (size_t i = total_PCM_frame_count; i < updated_size; ++i) {
      time[i] = static_cast<float>(i) / sample_rate;
      left_channel[i] = 0.0F;
      right_channel[i] = 0.0F;
    }

    drwav_free(pSampleData, nullptr);
    pSampleData = nullptr;
  }
  return true;
}

auto AudioData::getSectionOfData(Channel channel,
                                 float start_time,
                                 float end_time) -> std::span<const float>
{
  if (end_time <= start_time) {
    return {};
  }

  auto len = left_channel.size();
  size_t start_index = std::max<int64_t>(
      static_cast<int64_t>(start_time * static_cast<float>(sample_rate)), 0);
  size_t end_index = std::min<int64_t>(
      static_cast<int64_t>(end_time * static_cast<float>(sample_rate)), len);

  if (channel == Channel::LEFT) {
    return {left_channel.cbegin() + start_index,
            left_channel.cbegin() + end_index};
  } else {
    return {right_channel.cbegin() + start_index,
            right_channel.cbegin() + end_index};
  }
}
