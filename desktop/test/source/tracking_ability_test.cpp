#include <vector>

#include "tools/tracking_ability.hpp"

#include <catch2/catch_test_macros.hpp>

TEST_CASE("detects clipping signal 2 correctly", "[tracking_ability]")
{
  // Define the test input buffer and threshold
  std::vector<float> input_buffer = {
      0.1F,
      -0.2F,
      0.5F,
      -0.6F,  // Below threshold
      1.2F,
      -1.5F,  // Above threshold (clipping)
      0.9F,
      1.1F  // Above threshold (clipping)
  };
  float threshold = 1.0F;
  REQUIRE(tracking_ability::clipped(input_buffer, threshold));
}

TEST_CASE("detects clipping signal 1 correctly", "[tracking_ability]")
{
  // Define the test input buffer and threshold
  std::vector<float> input_buffer = {
      0.1F,
      -0.2F,
      0.5F,
      -0.6F,
      0.9F,
  };
  float threshold = 1.0F;
  REQUIRE(!tracking_ability::clipped(input_buffer, threshold));
}
