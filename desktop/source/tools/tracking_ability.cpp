#include <cstdlib>

#include "tracking_ability.hpp"

auto tracking_ability::clipped(std::span<const float> input_buffer,
                              float threshold) -> bool
{
  bool clipped = false;
  // Iterate over the input buffer in stereo pairs
  for (auto sample : input_buffer) {
    // Check for clipping based on the provided threshold
    clipped = std::abs(sample) > threshold;
  }
  return clipped;
}
