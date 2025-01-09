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
 * @file constants.hpp
 * @brief Header file for constants.
 *
 * @license GPL-3.0
 */

#include <cstddef>
namespace constants
{
constexpr size_t chunk_size = 2048;  // Number of frames per read
}  // namespace constants
