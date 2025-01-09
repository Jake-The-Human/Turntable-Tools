#pragma once

#include <complex>
#include <span>
#include <vector>

namespace dsp
{
/**
 * @brief Performs a Cooley-Tukey Fast Fourier Transform (FFT) on the data.
 *
 * This is a recursive implementation of the Cooley-Tukey FFT algorithm. It
 * divides the input data into even and odd indexed elements, recursively
 * calls FFT on them, and combines the results.
 *
 * @param data The input data, which will be transformed in place. The size
 * of the data must be a power of 2.
 */
auto fft(std::span<const float> data, bool enable_windowing)
    -> std::vector<std::complex<float>>;

auto ifft(const std::vector<std::complex<float>>& data) -> std::vector<float>;
}  // namespace dsp
