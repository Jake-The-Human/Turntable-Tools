// NOLINTBEGIN
#include <cmath>
#include <complex>
#include <numeric>
#include <vector>

#include "frequency_response.hpp"

#include <catch2/catch_test_macros.hpp>

TEST_CASE("Frequency Response Functionality", "[frequency_response]")
{
  frequency_response fr;
  std::vector<float> signal = {1.0f, 2.0f, 3.0f, 4.0f};
  fr.update(signal, 44100);
  REQUIRE(fr.frequency_response_map.size() > 0);

  // Check for known values (if possible) in the frequency response
  for (const auto& [freq, mag] : fr.frequency_response_map) {
    REQUIRE(mag >= -100.0f);  // Ensure magnitudes are within reasonable range
  }
}

TEST_CASE("Frequency Response - DC Signal", "[frequency_response]")
{
  frequency_response fr;
  std::vector<float> signal(1024, 1.0f);  // DC signal
  fr.update(signal, 44100);
  REQUIRE(fr.frequency_response_map.count(0.0f)
          == 1);  // Check for DC component
  REQUIRE(std::abs(fr.frequency_response_map.at(0.0f))
          > 0.0f);  // Check magnitude is positive
}

TEST_CASE("Frequency Response - Single Sine Wave", "[frequency_response]")
{
  frequency_response fr;
  uint32_t sample_rate = 44100;
  float frequency = 1000.0f;
  std::vector<float> signal(sample_rate);
  for (size_t i = 0; i < signal.size(); ++i) {
    signal[i] = std::sin(2.0f * std::numbers::pi_v<float>
                         * frequency * i / sample_rate);
  }

  for (size_t i = 0; i < signal.size() - 1024; i += 1024) {
    fr.update({&signal[i], &signal[i + 1024]}, sample_rate);
  }

  float expected_freq = frequency;
  bool found_peak = false;
  for (const auto& [freq, mag] : fr.frequency_response_map) {
    if (std::abs(freq - expected_freq) < 1.0f) {
      found_peak = true;
      REQUIRE(mag > -80.0f);  // Magnitude should be significant
      break;
    }
  }
  REQUIRE(found_peak);
}

TEST_CASE("Frequency Response - Clear Functionality", "[frequency_response]")
{
  frequency_response fr;
  std::vector<float> signal = {1.0f, 2.0f, 3.0f, 4.0f};
  fr.update(signal, 44100);
  REQUIRE(fr.frequency_response_map.size() > 0);
  fr.clear();
  REQUIRE(fr.frequency_response_map.empty());
}

TEST_CASE("Frequency Response - Nyquist Frequency", "[frequency_response]")
{
  frequency_response fr;
  uint32_t sample_rate = 44100;
  float frequency = sample_rate / 2.0f;  // Nyquist frequency
  std::vector<float> signal(sample_rate);
  for (size_t i = 0; i < signal.size(); ++i) {
    signal[i] = std::sin(2.0f * std::numbers::pi_v<float>
                         * frequency * i / sample_rate);
  }

  for (size_t i = 0; i < signal.size() - 1024; i += 1024) {
    fr.update({&signal[i], &signal[i + 1024]}, sample_rate);
  }

  bool found_peak = false;
  for (const auto& [freq, mag] : fr.frequency_response_map) {
    if (std::abs(freq - frequency) < 1.0f) {
      found_peak = true;
      REQUIRE(mag > -80.0f);  // Magnitude should be significant
      break;
    }
  }
  REQUIRE(found_peak);
}

// NOLINTEND
