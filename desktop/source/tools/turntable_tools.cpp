#include <cstdint>

#include "turntable_tools.hpp"

#include "tools/azimuth.hpp"
#include "tools/moving_avg.hpp"
#include "tools/thd.hpp"
#include "tools/tracking_ability.hpp"

turntable_tools::turntable_tools()
{
  m_azimuth_avg.avg_function =
      [](const std::array<azimuth::results, MOVING_AVG_SIZE>& input)
      -> azimuth::results
  {
    azimuth::results sum = {
        .crosstalk_signal_1 = 0, .crosstalk_signal_2 = 0, .phase_diff = 0};
    for (const auto& data : input) {
      sum.crosstalk_signal_1 += data.crosstalk_signal_1;
      sum.crosstalk_signal_2 += data.crosstalk_signal_2;
      sum.phase_diff += data.phase_diff;
    }

    return {.crosstalk_signal_1 = sum.crosstalk_signal_1 / MOVING_AVG_SIZE,
            .crosstalk_signal_2 = sum.crosstalk_signal_2 / MOVING_AVG_SIZE,
            .phase_diff = sum.phase_diff / MOVING_AVG_SIZE};
  };

  m_thd_avg.avg_function =
      [](const std::array<std::pair<float, float>, MOVING_AVG_SIZE>& input)
      -> std::pair<float, float>
  {
    std::pair<float, float> sum = {0, 0};
    for (const auto data : input) {
      sum.first += data.first;
      sum.second += data.second;
    }
    return {sum.first / MOVING_AVG_SIZE, sum.second / MOVING_AVG_SIZE};
  };
}

void turntable_tools::add_audio(std::span<float> left,
                                std::span<float> right,
                                uint32_t sample_rate)
{
  if (tests & static_cast<uint8_t>(tests::azimuth)) {
    m_azimuth_avg.update(
        azimuth::update(left, right, test_frequency, sample_rate));
  }

  if (tests & static_cast<uint8_t>(tests::frequency_response)) {
    m_freq_response.update(left, sample_rate);
    m_freq_response.update(right, sample_rate);
  }

  if (tests & static_cast<uint8_t>(tests::thd)) {
    m_thd_avg.update({thd::calculate(left), thd::calculate(right)});
  }

  if (tests & static_cast<uint8_t>(tests::tracking_ability)) {
    tracking_ability::clipped(left, 1.0F);
    tracking_ability::clipped(right, 1.0F);
  }
}
void turntable_tools::print_results() const {}
void turntable_tools::write_results_to_file(const std::string& path) const {}
