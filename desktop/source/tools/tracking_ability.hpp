#pragma once

#include <span>

/**
 * @brief namespace to define thresholds for detecting distortion or clipping.
 *
 * The thresholds represent different levels of distortion or clipping
 * that can occur due to lateral displacement. Lower thresholds represent
 * early signs of tracking difficulty, while higher thresholds indicate
 * significant clipping or severe distortion.
 */
namespace tracking_thresholds
{
constexpr auto low = 0.5F; /**< Low threshold (no distortion detected). */
constexpr auto medium = 0.8F; /**< Medium threshold (mild distortion). */
constexpr auto high =
    0.9F; /**< High threshold (likely clipping or severe distortion). */
}  // namespace tracking_thresholds

/**
 * @brief Class to simulate tracking ability based on lateral displacement.
 *
 * This class allows checking for clipping or distortion based on the amplitude
 * of the lateral displacement signals. It simulates the tracking ability of a
 * turntable and detects clipping or tracking failure by comparing signal
 * amplitudes against defined thresholds.
 */
namespace tracking_ability
{
/**
 * @brief Updates the tracking ability based on the input signal buffer.
 *
 * This method checks if the lateral displacement signals exceed the defined
 * thresholds, indicating possible clipping or distortion. It processes the
 * input signal buffer in stereo pairs (left and right channels).
 *
 * @param input_buffer The input signal buffer containing the audio data.
 *                      The buffer should be a sequence of floating-point
 * @param threshold The threshold value used to detect clipping or distortion.
 *                  The threshold can be one of the values from the
 * `thresholds` enum.
 */
auto clipped(std::span<const float> input_buffer, float threshold) -> bool;
};  // namespace tracking_ability
