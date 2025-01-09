#include <cstddef>
#include <iostream>
#include <span>
#include <vector>

// NOLINTBEGIN
#include <argparse/argparse.hpp>
#include <miniaudio.h>
// NOLINTEND

#include "azimuth.hpp"
#include "constants.hpp"
#include "frequency_response.hpp"
#include "thd.hpp"
#include "tracking_ability.hpp"

constexpr auto INPUT_FILES_ARG = "--input-files";  // Thanks Dabe

auto main(int argc, char* argv[]) -> int
{
  argparse::ArgumentParser program("TurntableTools");
  program.add_argument(INPUT_FILES_ARG)
      .help("Files you want to test in flac or wave format")
      .nargs(argparse::nargs_pattern::at_least_one);

  try {
    program.parse_args(argc, argv);
  } catch (const std::exception& err) {
    std::cerr << err.what() << '\n';
    std::cerr << program;
    return 1;
  }

  ma_decoder decoder;
  ma_decoder_config config = ma_decoder_config_init(ma_format_f32, 2, 48000);
  ma_format format;
  ma_uint32 channels;
  ma_uint32 sample_rate;

  for (const auto& file :
       program.get<std::vector<std::string>>(INPUT_FILES_ARG))
  {
    std::cout << "Now processing: " << file << '\n';
    ma_result result = ma_decoder_init_file(file.c_str(), &config, &decoder);
    if (result != MA_SUCCESS) {
      std::cout << "Error: Failed to read/decode check path and format: "
                << file << '\n';
      return 1;
    }

    channels = decoder.outputChannels;
    sample_rate = decoder.outputSampleRate;
    format = decoder.outputFormat;
    std::cout << "Number of channels: " << channels << '\n'
              << "Sampling Rate: " << sample_rate << '\n';

    std::vector<float> signal_1(constants::chunk_size / 2);
    std::vector<float> signal_2(constants::chunk_size / 2);
    uint32_t test_freq = 1000;

    azimuth azi;
    tracking_ability t_a_test;
    frequency_response f_r_test_1;
    frequency_response f_r_test_2;

    std::vector<std::byte> buffer(constants::chunk_size
                                  * ma_get_bytes_per_frame(format, channels));
    ma_uint64 frames_read = 0;
    while (ma_decoder_read_pcm_frames(
               &decoder, buffer.data(), constants::chunk_size, &frames_read)
           == MA_SUCCESS)
    {
      auto data_span = std::span<const float> {
          reinterpret_cast<const float*>(buffer.data()), constants::chunk_size};

      // Split the stereo signal into left and right channels
      for (size_t i = 0; i < data_span.size() / 2; ++i) {
        signal_1.at(i) = data_span[2 * i];  // Left channel
        signal_2.at(i) = data_span[(2 * i) + 1];  // Right channel
      }

      azi.update(signal_1, signal_2, test_freq, sample_rate);
      std::cout << "crosstalk on 1: " << azi.crosstalk_signal_1
                << " dB\ncrosstalk on 2: " << azi.crosstalk_signal_2
                << " dB\nphase diff: " << azi.phase_diff << " Degrees\n";

      std::cout << "THD on 1: " << thd::calculate(signal_1)
                << " %\nTHD on 2: " << thd::calculate(signal_2) << " %\n";
      t_a_test.update(data_span, tracking_thresholds::medium);
      std::cout << "Clipped on 1: " << t_a_test.signal_1_clipped
                << "\nClipped on 2: " << t_a_test.signal_2_clipped << "\n";
      f_r_test_1.update(signal_1, sample_rate);
      f_r_test_2.update(signal_2, sample_rate);
    }

    auto peak_1 = f_r_test_1.findMaxFrequency();
    auto peak_2 = f_r_test_2.findMaxFrequency();
    std::cout << "Channel 1 fundamental freq: " << peak_1.first << " Hz "
              << peak_1.second << " dB" << '\n';
    std::cout << "Channel 2 fundamental freq: " << peak_2.first << " Hz "
              << peak_2.second << " dB" << '\n';

    ma_decoder_uninit(&decoder);
  }
  return 0;
}
