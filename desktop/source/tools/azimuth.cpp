#include <cmath>

#include "azimuth.hpp"

#include "phase.hpp"

namespace
{
/**
 * @brief Converts crosstalk signal ratio to decibels.
 *
 * This function calculates the crosstalk in decibels between two signals.
 * If the main signal is zero, it returns 0 decibels.
 *
 * @param main_signal The main signal amplitude.
 * @param secondary_signal The secondary signal amplitude.
 * @return The crosstalk in decibels.
 */
constexpr auto crosstalk_in_db(float main_signal, float secondary_signal)
    -> float
{
  constexpr float epsilon = 1e-12F;  // Small value to prevent division by zero
  return 20.0F * std::log10(secondary_signal / (main_signal + epsilon));
}

/**
 * @brief Calculates the root mean square (RMS) of a signal.
 *
 * This function calculates the RMS of a given signal, which is a measure of
 * the signal's magnitude.
 *
 * @param data A span of floating-point data representing the signal.
 * @return The RMS value of the signal.
 */
constexpr auto rms(const std::span<const float> data) -> float
{
  float sum = 0.0F;
  for (size_t i = 0; i < data.size(); i += 1) {
    sum += data[i] * data[i];
  }

  return std::sqrt(sum / static_cast<float>(data.size()));
}
}  // namespace

auto azimuth::update(std::span<const float> signal_1,
                     std::span<const float> signal_2,
                     uint32_t frequency,
                     uint32_t sampling_rate) -> azimuth::Results
{
  const float rms_signal_1 = rms(signal_1);
  const float rms_signal_2 = rms(signal_2);

  return {.crosstalk_signal_1 = crosstalk_in_db(rms_signal_1, rms_signal_2),
          .crosstalk_signal_2 = crosstalk_in_db(rms_signal_2, rms_signal_1),
      .phase_diff = 0
      // phase::calculate_difference(signal_1,
      //                             signal_2,
      //                             frequency,
      //                             sampling_rate)  // !NOTE: if signal is not
      // a power of 2 fix that
  };
}
