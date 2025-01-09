#pragma once

#include <string>

/**
 * @brief The core implementation of the executable
 *
 * This class makes up the library part of the executable, which means that the
 * main logic is implemented here. This kind of separation makes it easy to
 * test the implementation for the executable, because the logic is nicely
 * separated from the command-line logic implemented in the main function.
 */
struct library
{
  /**
   * @brief Simply initializes the name member to the name of the project
   */
  library();

  std::string name;
};

// template<typename T, size_t N>
// struct moving_average
// {
//   auto uptdate(T sample)
//   {
//     data.at(index) = sample;
//     index = get_next_index(index, data.size());

//     size_t sum = 0;
//     for (auto data_sample : data) {
//       sum += static_cast<size_t>(data_sample);
//     }

//     return static_cast<T>(sum / data.size());
//   }

//   size_t index = 0;
//   std::array<T, N> data = {0};
// };
