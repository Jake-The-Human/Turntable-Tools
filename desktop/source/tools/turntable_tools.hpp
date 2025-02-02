#pragma once

#include <cstdint>
#include <span>
#include <string>

#include "tools/azimuth.hpp"
#include "tools/frequency_response.hpp"
#include "tools/moving_avg.hpp"
#include "tools/thd.hpp"

struct turntable_tools
{
  ~turntable_tools() = default;
  turntable_tools();
  turntable_tools(const turntable_tools&) = default;
  turntable_tools(turntable_tools&&) = default;
  auto operator=(const turntable_tools&) -> turntable_tools& = default;
  auto operator=(turntable_tools&&) -> turntable_tools& = default;
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
  void print_results() const;
  void write_results_to_file(const std::string& path) const;

  uint8_t tests = 0;
  uint32_t test_frequency = 1;
  frequency_response m_freq_response;

private:
  moving_average<azimuth::results, MOVING_AVG_SIZE> m_azimuth_avg;
  moving_average<std::pair<float, float>, MOVING_AVG_SIZE> m_thd_avg;

};
