#include <cstdlib>

#include "tracking_ability.hpp"

void tracking_ability::update(std::span<const float> input_buffer,
                              float threshold)
{
  // Iterate over the input buffer in stereo pairs
  for (size_t i = 0; i < input_buffer.size() / 2; ++i) {
    // Check for clipping based on the provided threshold
    signal_1_clipped = std::abs(input_buffer[2 * i]) > threshold;
    signal_2_clipped = std::abs(input_buffer[(2 * i) + 1]) > threshold;
  }
}
