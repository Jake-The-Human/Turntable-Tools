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
 * @file thd.hpp
 * @brief Header file for calculating Total Harmonic Distortion (THD) from audio
 * signals.
 *
 * With Ortofon test record you can use Tracks 5 - 8 one at a time to test the
 * distortion on the left and right channel.
 *
 * This file contains functions and structures to process stereo audio signals
 * and calculate Total Harmonic Distortion (THD) for both left and right
 * channels. It utilizes Fast Fourier Transform (FFT) to analyze the harmonic
 * content of the input signals and compute THD.
 *
 * @license GPL-3.0
 */

#include <span>

namespace thd
{
/**
 * @brief Calculate a single channel (left or right) by performing FFT and
 * calculating THD (Total Harmonic Distortion).
 *
 * This function first converts the input signal into a complex signal (real
 * part is the signal, imaginary part is zero), performs an FFT, and then
 * calculates the THD by comparing the magnitudes of harmonic frequencies
 * (bins 2-5) to the fundamental frequency (bin 1).
 *
 * @param channel The input signal (either left or right channel).
 * @return The THD measurement for the channel.
 */
auto calculate(std::span<const float> input_buffer) -> float;
}  // namespace thd
