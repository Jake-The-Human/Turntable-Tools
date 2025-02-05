#include <cmath>
#include <complex>
#include <iostream>
#include <vector>

#include "frequency_response.hpp"

#include "fft.hpp"

void FrequencyResponse::update(std::span<const float> signal,
                               uint32_t sample_rate)
{
  const size_t num_samples = signal.size();

  // Perform FFT on the signal
  auto complex_signal = dsp::fft(signal, true);

  // Calculate magnitude (in dB) and phase (in degrees)
  for (size_t i = 0; i < num_samples / 2; ++i) {
    const float magnitude = std::abs(complex_signal[i]);
    const float magnitude_db = 20.0F * std::log10(std::max(magnitude, 1e-12F));

    const float phase =
        std::arg(complex_signal[i]) * 180.0F / M_PI;  // Convert to degrees

    const float frequency = static_cast<float>(i)
        * static_cast<float>(sample_rate) / static_cast<float>(num_samples);

    // Store values
    frequency_response_map[frequency] = {magnitude_db, phase};
  }
}

// void FrequencyResponse::display_response(const std::string& label) const
// {
//   for (const auto& [freq, mag_db] : frequency_response_map) {
//     std::cout << label << " Frequency: " << freq << " Hz, Magnitude: " <<
//     mag_db
//               << " dB" << '\n';
//   }
// }

// auto FrequencyResponse::find_max_frequency() const -> std::pair<float, float>
// {
//   float max_freq = 0.0F;
//   float max_magnitude = 0.0F;
//   for (const auto& [freq, mag_db] : frequency_response_map) {
//     if (mag_db > max_magnitude) {
//       max_magnitude = mag_db;
//       max_freq = freq;
//     }
//   }
//   return {max_freq, max_magnitude};
// }
