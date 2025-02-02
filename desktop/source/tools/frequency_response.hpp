#pragma once

#include <cstdint>
#include <map>
#include <span>
#include <string>

struct frequency_response
{
  /**
   * @brief Calculates the frequency response of the input signal using FFT.
   *
   * This method computes the frequency response by performing an FFT on the
   * input signal and calculating the magnitudes in decibels for the frequency
   * bins.
   *
   * @param signal The input time-domain signal.
   * @param sample_rate The sample rate of the input signal.
   */
  void update(std::span<const float> signal, uint32_t sample_rate);

  /**
   * @brief Displays the frequency response (frequencies and their magnitudes in
   * dB).
   *
   * @param label The helps identify the data.
   */
  void display_response(const std::string& label) const;

  auto find_max_frequency() const -> std::pair<float, float>;

  /**
   * @brief clears the internal frequency response data so you can do another
   * measurement.
   */
  void clear() { frequency_response_map.clear(); }

  std::map<float, float>
      frequency_response_map; /**< Stores frequencies and their corresponding
                                   magnitudes in dB. */
};
