#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <numbers>
#include <span>
#include <vector>

#include "phase.hpp"

namespace
{

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
 * @brief Calculates the cross-correlation between two signals.
 *
 * This function calculates the cross-correlation between two signals,
 * which helps determine their similarity over time.
 *
 * @param signal1 The first signal.
 * @param signal2 The second signal.
 * @return A vector containing the cross-correlation values.
 */
constexpr auto cross_correlation(std::span<const float> signal1,
                                 std::span<const float> signal2)
    -> std::vector<float>
{
  if (signal1.size() != signal2.size()) {
    return {};
  }

  auto N = static_cast<int64_t>(signal1.size());
  std::vector<float> result(static_cast<size_t>(2 * N) - 1, 0.0F);

  for (int64_t lag = -(N - 1); lag < N; ++lag) {
    float sum = 0.0F;
    for (int64_t i = 0; i < N; ++i) {
      int64_t j = i + lag;
      if (j >= 0 && j < N) {
        sum +=
            signal1[static_cast<size_t>(i)] * signal2[static_cast<size_t>(j)];
      }
    }
    result[static_cast<size_t>(lag + (N - 1))] = sum;
  }
  return result;
}

/**
 * @brief Finds the time lag corresponding to the maximum cross-correlation.
 *
 * This function finds the index of the maximum cross-correlation value,
 * which represents the time lag between two signals.
 *
 * @param correlation The cross-correlation values.
 * @return The time lag corresponding to the maximum correlation.
 */
constexpr auto find_time_lag(const std::vector<float>& correlation)
    -> std::ptrdiff_t
{
  auto max_iter = std::ranges::max_element(correlation);
  auto max_index = std::distance(correlation.begin(), max_iter);
  auto zero_lag_index = static_cast<std::ptrdiff_t>(correlation.size() / 2);
  return max_index - zero_lag_index;
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
