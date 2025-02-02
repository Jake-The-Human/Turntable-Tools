#include <algorithm>
#include <complex>
#include <numbers>
#include <vector>

#include "fft.hpp"

#include <pocketfft_hdronly.h>

/**
 * @brief Computes the Hamming window value at each index.
 *
 * The Hamming window is used to reduce spectral leakage when performing a
 * Fourier Transform. It applies a cosine function that tapers the signal
 * smoothly towards the edges.
 *
 * @param index The index of the sample in the window.
 * @param window_size The size of the window.
 * @return The window value at the specified index.
 */
constexpr auto hamming(size_t index, size_t window_size) -> float
{
  if (window_size == 1) {
    return 1.0f;  // For a single point, the window value is trivially 1.
  }
  constexpr float alpha = 0.54F;
  constexpr float beta = 0.46F;
  return alpha
      - (beta
         * std::cos(2 * std::numbers::pi_v<float> * index / (window_size - 1)));
}

auto dsp::fft(std::span<const float> data, bool enable_windowing)
    -> std::vector<std::complex<float>>
{
  // Copy data and apply windowing if enabled
  std::vector<float> windowed_signal(data.begin(), data.end());
  if (enable_windowing) {
    for (size_t i = 0; i < windowed_signal.size(); ++i) {
      // Apply Hamming window
      windowed_signal[i] *= hamming(i, windowed_signal.size());
    }
  }

  // Convert to complex data (real part is the windowed signal, imaginary is 0)
  std::vector<std::complex<float>> complex_data(windowed_signal.size());
  for (size_t i = 0; i < windowed_signal.size(); ++i) {
    complex_data[i] = {windowed_signal[i], 0.0F};
  }

  // Define FFT parameters
  pocketfft::shape_t shape = {complex_data.size()};
  pocketfft::stride_t stride_in = {sizeof(float)};
  pocketfft::stride_t stride_out = {sizeof(std::complex<float>)};
  pocketfft::shape_t axes = {0};

  // Perform FFT
  pocketfft::r2c(shape,
                 stride_in,
                 stride_out,
                 axes,
                 true,
                 windowed_signal.data(),
                 complex_data.data(),
                 1.0F);

  return complex_data;
}

auto dsp::ifft(const std::vector<std::complex<float>>& data)
    -> std::vector<float>
{
  std::vector<float> real_result(data.size());

  // Define IFFT parameters
  pocketfft::shape_t shape = {data.size()};
  pocketfft::stride_t stride_in = {sizeof(std::complex<float>)};
  pocketfft::stride_t stride_out = {sizeof(float)};
  pocketfft::shape_t axes = {0};

  // Perform IFFT
  pocketfft::c2r(shape,
                 stride_in,
                 stride_out,
                 axes,
                 false,
                 data.data(),
                 real_result.data(),
                 1.0F / static_cast<float>(data.size()));

  return real_result;
}
