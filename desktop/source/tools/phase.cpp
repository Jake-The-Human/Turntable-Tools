#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <numbers>
#include <span>
#include <vector>

#include "phase.hpp"

#include "fft.hpp"

namespace
{

// Utility function: returns the next power of two that is at least n.
inline size_t next_power_of_two(size_t n)
{
  size_t power = 1;
  while (power < n) {
    power *= 2;
  }
  return power;
}

/**
 * @brief Calculates the phase difference between two signals.
 *
 * This function calculates the phase difference in degrees based on the
 * time lag between two signals, the signal frequency, and the sampling rate.
 *
 * @param lag The time lag between the signals.
 * @param frequency The frequency of the signal.
 * @param sampling_rate The sampling rate of the signals.
 * @return The phase difference in degrees.
 */
constexpr auto calculate_phase_difference(std::ptrdiff_t lag,
                                          uint32_t frequency,
                                          uint32_t sampling_rate) -> float
{
  float time_shift =
      static_cast<float>(lag) / static_cast<float>(sampling_rate);
  float period = 1.0F / static_cast<float>(frequency);
  float phase_difference_radians =
      (time_shift / period) * 2 * std::numbers::pi_v<float>;
  float phase_difference_degrees =
      phase_difference_radians * 180.0F / std::numbers::pi_v<float>;

  while (phase_difference_degrees > 180.0F) {
    phase_difference_degrees -= 360.0F;
  }
  while (phase_difference_degrees < -180.0F) {
    phase_difference_degrees += 360.0F;
  }

  return phase_difference_degrees;
}

/**
 * @brief Computes the cross-correlation between two signals using FFTs.
 *
 * This function computes the cross-correlation by zero-padding the signals,
 * computing their FFTs (with windowing disabled), multiplying one FFT by the
 * conjugate of the other, and then computing the inverse FFT.
 *
 * @param signal1 The first input signal.
 * @param signal2 The second input signal.
 * @return A vector containing the cross-correlation of the two signals. The
 *         length of the returned vector is (2 * N - 1), with zero lag at index
 * N-1.
 */
std::vector<float> cross_correlation(std::span<const float> signal1,
                                     std::span<const float> signal2)
{
  // Ensure signals are of equal length.
  if (signal1.size() != signal2.size()) {
    return {};
  }

  const size_t N = signal1.size();
  // The linear cross-correlation length is 2*N - 1.
  const size_t corrLength = 2 * N - 1;
  // Choose an FFT size that is a power of two and at least as large as
  // corrLength.
  const size_t fftSize = next_power_of_two(corrLength);

  // Zero-pad the signals to length fftSize.
  std::vector<float> padded1(fftSize, 0.0f);
  std::vector<float> padded2(fftSize, 0.0f);
  std::copy(signal1.begin(), signal1.end(), padded1.begin());
  std::copy(signal2.begin(), signal2.end(), padded2.begin());

  // Compute FFTs using your fft function (disable windowing for correlation).
  auto fft1 = dsp::fft(padded1, false);
  auto fft2 = dsp::fft(padded2, false);

  // Multiply fft1 by the complex conjugate of fft2 element-wise.
  std::vector<std::complex<float>> product(fftSize);
  for (size_t i = 0; i < fftSize; ++i) {
    product[i] = fft1[i] * std::conj(fft2[i]);
  }

  // Compute the inverse FFT to obtain the circular cross-correlation.
  auto ifftResult = dsp::ifft(product);

  // Because of the way the FFT-based correlation works, the zero lag
  // (i.e. no shift) is located at index N-1.
  // Extract the valid linear cross-correlation values (length = 2*N - 1)
  // and re-order them so that negative lags come first.
  std::vector<float> correlation(corrLength);
  for (size_t i = 0; i < corrLength; ++i) {
    // Shifting by (N - 1) ensures that correlation[0] corresponds to lag =
    // -(N-1) and correlation[corrLength-1] corresponds to lag = N-1.
    size_t index = (i + N - 1) % fftSize;
    correlation[i] = ifftResult[index];
  }

  return correlation;
}

constexpr auto find_time_lag(const std::vector<float>& correlation) -> float
{
  // Find the index of the maximum element.
  auto max_iter = std::ranges::max_element(correlation);
  size_t max_index = std::distance(correlation.begin(), max_iter);
  const float max_value = *max_iter;

  // Zero-lag is assumed to be at the center of the correlation vector.
  float zero_lag_index = static_cast<float>(correlation.size()) / 2.0F;

  // Initialize the fractional offset to zero.
  float d = 0.0F;
  // Perform parabolic interpolation only if the maximum is not at the edges.
  if (max_index > 0 && max_index < correlation.size() - 1) {
    float left  = correlation[max_index - 1];
    float right = correlation[max_index + 1];
    float denominator = left - 2.0F * max_value + right;
    if (denominator != 0.0F) {
      d = 0.5F * (left - right) / denominator;
    }
  }
  // Return the refined lag (which can be fractional)
  return (static_cast<float>(max_index) + d) - zero_lag_index;
}


}  // namespace

auto phase::calculate_difference(std::span<const float> signal_1,
                                 std::span<const float> signal_2,
                                 uint32_t frequency,
                                 uint32_t sampling_rate) -> float
{
  auto correlation = cross_correlation(signal_1, signal_2);
  // Find the time lag corresponding to the maximum correlation
  if (correlation.empty()) {
    return 0.0F;
  }

  auto time_lag = find_time_lag(correlation);
  return calculate_phase_difference(time_lag, frequency, sampling_rate);
}
