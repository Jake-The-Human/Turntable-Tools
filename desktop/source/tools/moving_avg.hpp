#pragma once

#include <array>
#include <cstddef>
#include <functional>

constexpr auto MOVING_AVG_SIZE = 10;

template<typename T, size_t N>
struct moving_average
{
  auto update(const T& input_data) -> T
  {
    index = (index + 1) % data.size();
    data.at(index) = input_data;
    return avg_function(data);
  }

  size_t index = -1;
  std::function<T(const std::array<T, N>&)> avg_function;
  std::array<T, N> data;
};
