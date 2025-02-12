#pragma once

#include <cstdint>
#include <span>

#include "azimuth.hpp"
#include "frequency_response.hpp"
#include "moving_avg.hpp"

struct TurntableTools
{
  ~TurntableTools() = default;
  TurntableTools();
  TurntableTools(const TurntableTools&) = default;
  TurntableTools(TurntableTools&&) = default;
  auto operator=(const TurntableTools&) -> TurntableTools& = default;
  auto operator=(TurntableTools&&) -> TurntableTools& = default;
  enum class tests : uint8_t
  {
    azimuth = 1,
    frequency_response = 2,
    thd = 4,
    tracking_ability = 8,
  };
  void add_audio(std::span<float> left,
                 std::span<float> right,
                 uint32_t sample_rate);

  uint8_t tests = 0;
  uint32_t test_frequency = 1;
  FrequencyResponse freq_response;
  MovingAverage<azimuth::Results, MOVING_AVG_SIZE> azimuth_avg;
  MovingAverage<std::pair<float, float>, MOVING_AVG_SIZE> thd_avg;
};
