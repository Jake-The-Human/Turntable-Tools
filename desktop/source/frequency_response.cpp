#include <cmath>
#include <complex>
#include <iostream>
#include <vector>

#include "frequency_response.hpp"

#include "fft.hpp"

void frequency_response::update(std::span<const float> signal,
                                uint32_t sample_rate)
{
  const size_t num_samples = signal.size();

  // Perform FFT on the signal
  auto complex_signal = dsp::fft(signal, true);

  // Calculate the magnitude (in dB) for each frequency bin
  for (size_t i = 1; i < num_samples / 2; ++i)
  {  // Only need the positive frequencies
    const float magnitude = std::abs(complex_signal[i]);

    // Convert magnitude to decibels
    const float magnitude_db =
        20.0F * std::log10(magnitude + 1e-12F);  // Add epsilon to avoid log(0)

    // Calculate corresponding frequency (bin index * sample rate / total
    // number of bins)
    const float frequency = static_cast<float>(i)
        * static_cast<float>(sample_rate) / static_cast<float>(num_samples);

    // Store the frequency and its corresponding magnitude in the map
    frequency_response_map[frequency] = magnitude_db;
  }
}

void frequency_response::display_response(const std::string& label) const
{
  for (const auto& [freq, mag_db] : frequency_response_map) {
    std::cout << label << " Frequency: " << freq << " Hz, Magnitude: " << mag_db
              << " dB" << '\n';
  }
}

auto frequency_response::findMaxFrequency() const -> std::pair<float, float>
{
  float max_freq = 0.0F;
  float max_magnitude = 0.0F;
  for (const auto& [freq, mag_db] : frequency_response_map) {
    if (mag_db > max_magnitude) {
      max_magnitude = mag_db;
      max_freq = freq;
    }
  }
  return {max_freq, max_magnitude};
}
