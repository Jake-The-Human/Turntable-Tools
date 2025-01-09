#include <vector>

#include "tracking_ability.hpp"

#include <catch2/catch_test_macros.hpp>

TEST_CASE("detects clipping signal 2 correctly", "[tracking_ability]")
{
  // Create an instance of tracking_ability
  tracking_ability tracker;

  // Define the test input buffer and threshold
  std::vector<float> input_buffer = {
      0.1f,
      -0.2f,
      0.5f,
      -0.6f,  // Below threshold
      1.2f,
      -1.5f,  // Above threshold (clipping)
      0.9f,
      1.1f  // Above threshold (clipping)
  };
  float threshold = 1.0f;

  tracker.update(input_buffer, threshold);

  REQUIRE(!tracker.signal_1_clipped);
  REQUIRE(tracker.signal_2_clipped);
}

TEST_CASE("detects clipping signal 1 correctly", "[tracking_ability]")
{
  // Create an instance of tracking_ability
  tracking_ability tracker;

  // Define the test input buffer and threshold
  std::vector<float> input_buffer = {
      0.1f,
      -0.2f,
      0.5f,
      -0.6f,
      -1.5f,  // Above threshold (clipping)
      1.2f,
      1.1f,  // Above threshold (clipping)
      0.9f,
  };
  float threshold = 1.0f;

  tracker.update(input_buffer, threshold);

  REQUIRE(tracker.signal_1_clipped);
  REQUIRE(!tracker.signal_2_clipped);
}
