#include <algorithm>
#include <complex>
#include <vector>

#include "thd.hpp"

#include "fft.hpp"

namespace
{
auto findHarmonicPeaks(const std::vector<std::complex<float>>& spectrum,
                       size_t fundamental_bin) -> std::vector<size_t>
{
  std::vector<size_t> harmonic_peaks;

  // Calculate magnitude spectrum
  std::vector<float> magnitude_spectrum(spectrum.size());
  std::transform(spectrum.begin(),
                 spectrum.end(),
                 magnitude_spectrum.begin(),
                 [](const std::complex<float>& c) { return std::abs(c); });

  // Find local maxima (peaks)
  for (size_t i = fundamental_bin * 2; i < magnitude_spectrum.size(); ++i) {
    if (i > 0 && i < magnitude_spectrum.size() - 1
        && magnitude_spectrum[i] > magnitude_spectrum[i - 1]
        && magnitude_spectrum[i] > magnitude_spectrum[i + 1])
    {
      harmonic_peaks.push_back(i);
    }
  }

  // Filter peaks based on a threshold (adjust as needed)
  const float peak_threshold =
      0.1 * magnitude_spectrum[fundamental_bin];  // Example threshold
  harmonic_peaks.erase(
      std::remove_if(harmonic_peaks.begin(),
                     harmonic_peaks.end(),
                     [&magnitude_spectrum, peak_threshold](size_t i)
                     { return magnitude_spectrum[i] < peak_threshold; }),
      harmonic_peaks.end());

  return harmonic_peaks;
}
}  // namespace

auto thd::calculate(std::span<const float> input_buffer) -> float
{
  auto complex_signal = dsp::fft(input_buffer, true);

  // Find the bin with the maximum magnitude (fundamental frequency)
  size_t fundamental_bin = 0;
  float fundamental_magnitude = 0.0F;
  for (size_t i = 1; i < complex_signal.size() / 2; ++i) {
    float magnitude = std::abs(complex_signal[i]);
    if (magnitude > fundamental_magnitude) {
      fundamental_magnitude = magnitude;
      fundamental_bin = i;
    }
  }

  auto harmonic_peaks = findHarmonicPeaks(complex_signal, fundamental_bin);

  float harmonic_sum_of_squares = 0.0F;
  for (size_t harmonic_bin : harmonic_peaks) {
    harmonic_sum_of_squares +=
        std::pow(std::abs(complex_signal[harmonic_bin]), 2);
  }

  float harmonics_rms =
      std::sqrt(harmonic_sum_of_squares / harmonic_peaks.size());

  // Calculate THD ratio (harmonic sum / fundamental magnitude), expressed as
  // percentage
  if (fundamental_magnitude > 0) {
    return (harmonics_rms / fundamental_magnitude) * 100.0F;
  }

  return 0.0F;  // If no fundamental was detected, return 0 THD
}
