#include <algorithm>
#include <cmath>
#include <complex>
#include <stdexcept>
#include <vector>

#include "thd.hpp"

#include "fft.hpp"

namespace
{
/**
 * @brief Finds the harmonic peaks in a frequency spectrum.
 *
 * This function computes the magnitude spectrum from a vector of complex
 * values, then searches for local maxima (i.e. bins that are larger than their
 * immediate neighbors) starting from twice the fundamental bin. Only peaks
 * above a threshold (a fraction of the magnitude at the fundamental bin) are
 * returned.
 *
 * @param spectrum A vector of complex numbers representing the frequency
 * spectrum.
 * @param fundamental_bin The bin corresponding to the fundamental frequency.
 * @param threshold_ratio The fraction of the fundamental magnitude that a peak
 * must exceed to be considered valid. Default is 0.1.
 * @return A vector of indices corresponding to detected harmonic peaks.
 *
 * @throws std::invalid_argument if fundamental_bin is not within the valid
 * range.
 */
auto findHarmonicPeaks(const std::vector<std::complex<float>>& spectrum,
                       size_t fundamental_bin,
                       float threshold_ratio = 0.1f) -> std::vector<size_t>
{
  // Validate fundamental_bin.
  if (spectrum.empty() || fundamental_bin >= spectrum.size()) {
    throw std::invalid_argument(
        "Invalid fundamental_bin: it must be within the spectrum range.");
  }

  // Compute the magnitude spectrum.
  std::vector<float> magnitude_spectrum;
  magnitude_spectrum.reserve(spectrum.size());
  for (const auto& c : spectrum) {
    magnitude_spectrum.push_back(std::abs(c));
  }

  // Determine the starting index for searching for harmonic peaks.
  // We assume harmonics will be found above the first harmonic (i.e. starting
  // at 2 * fundamental_bin).
  size_t start_index = fundamental_bin * 2;
  if (start_index < 1)
  {  // safeguard, though fundamental_bin is expected to be nonzero.
    start_index = 1;
  }

  std::vector<size_t> harmonic_peaks;
  // Loop through the spectrum, ensuring we have neighbors to compare against.
  // We stop at size()-1 because we compare each element with the element after
  // it.
  for (size_t i = start_index; i < magnitude_spectrum.size() - 1; ++i) {
    // Check if the current bin is a local maximum.
    if (magnitude_spectrum[i] > magnitude_spectrum[i - 1]
        && magnitude_spectrum[i] > magnitude_spectrum[i + 1])
    {
      harmonic_peaks.push_back(i);
    }
  }

  // Compute a threshold based on the magnitude at the fundamental bin.
  const float fundamental_magnitude = magnitude_spectrum[fundamental_bin];
  const float peak_threshold = threshold_ratio * fundamental_magnitude;

  // Remove peaks that do not exceed the threshold.
  harmonic_peaks.erase(
      std::remove_if(harmonic_peaks.begin(),
                     harmonic_peaks.end(),
                     [&](size_t idx)
                     { return magnitude_spectrum[idx] < peak_threshold; }),
      harmonic_peaks.end());

  return harmonic_peaks;
}

}  // namespace

auto thd::calculate(std::span<const float> input_buffer) -> float
{
  // Check for empty input
  if (input_buffer.empty()) {
    return 0.0F;
  }

  // Compute the FFT (windowing disabled)
  auto complex_signal = dsp::fft(input_buffer, true);

  // Find the fundamental frequency bin (ignoring DC)
  size_t fundamental_bin = 0;
  float fundamental_magnitude = 0.0F;
  // For real signals, only the first half of the spectrum is unique.
  for (size_t i = 1; i < complex_signal.size() / 2; ++i) {
    float magnitude =
        std::abs(complex_signal[i]) * dsp::hamming_gain_correction;
    if (magnitude > fundamental_magnitude) {
      fundamental_magnitude = magnitude;
      fundamental_bin = i;
    }
  }

  // If the fundamental magnitude is zero (or nearly zero), return 0 THD.
  if (fundamental_magnitude <= 0.0F) {
    return 0.0F;
  }

  // Identify harmonic peaks (using the improved findHarmonicPeaks function)
  auto harmonic_peaks = findHarmonicPeaks(complex_signal, fundamental_bin);

  // Avoid division by zero if no harmonics are found.
  if (harmonic_peaks.empty()) {
    return 0.0F;
  }

  // Sum the squared magnitudes of the detected harmonic bins.
  float harmonic_sum_of_squares = 0.0F;
  for (size_t harmonic_bin : harmonic_peaks) {
    harmonic_sum_of_squares +=
        std::pow(std::abs(complex_signal[harmonic_bin]), 2);
  }

  // Use the total harmonic power, not the average.
  float harmonics_total_rms = std::sqrt(harmonic_sum_of_squares);

  // Then compute THD as a ratio to the fundamental amplitude.
  float thd_percentage = (harmonics_total_rms / fundamental_magnitude) * 100.0F;

  return thd_percentage;
}
