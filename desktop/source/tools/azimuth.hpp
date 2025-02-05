#pragma once

/*
 * Copyright (C) 2025 Jake The Human
 *
 * This file is part of the Turntable Tools project.
 *
 * Turntable Tools is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Turntable Tools is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Turntable Tools. If not, see <https://www.gnu.org/licenses/>.
 */

/**
 * @file azimuth.hpp
 * @brief Header file for signal processing utilities, including crosstalk, RMS,
 * phase difference, and cross-correlation calculations.
 *
 * With Ortofon test record you can use Tracks 5 - 8 one at a time to test the
 * distortion on the left and right channel.
 *
 * This file contains utility functions and a template structure to compute
 * crosstalk in decibels, root mean square (RMS) values, phase difference, and
 * cross-correlation for stereo audio signals. The azimuth structure helps
 * process stereo signal pairs and computes related metrics such as crosstalk,
 * phase difference, and correlation-based time lag.
 *
 * @license GPL-3.0
 */

#include <cstdint>
#include <span>

namespace azimuth
{
struct Results
{
  float crosstalk_signal_1 = 0; /**< The crosstalk for signal 1 in dB. */
  float crosstalk_signal_2 = 0; /**< The crosstalk for signal 2 in dB. */
  float phase_diff = 0; /**< The phase difference in degrees. */
};

/**
 * @brief Updates the azimuth with the input signal and calculates related
 * metrics.
 *
 * This method updates the internal signal buffers and calculates the RMS,
 * crosstalk, and phase difference between the signals based on the provided
 * input buffer, frequency, and sampling rate.
 *
 * @param input_buffer The input buffer containing the signals.
 * @param frequency The frequency of the signals.
 * @param sampling_rate The sampling rate of the signals.
 */
auto update(std::span<const float> signal_1,
            std::span<const float> signal_2,
            uint32_t frequency,
            uint32_t sampling_rate) -> Results;
};  // namespace azimuth
