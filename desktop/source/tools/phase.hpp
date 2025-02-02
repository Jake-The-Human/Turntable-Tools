#pragma once

#include <cstdint>
#include <span>

namespace phase
{
auto calculate_difference(std::span<const float> signal_1,
                          std::span<const float> signal_2,
                          uint32_t frequency,
                          uint32_t sampling_rate) -> float;
} // namespace phase
