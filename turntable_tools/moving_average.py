"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: moving_average.py
Description: This file is the moving avg logic that is used to de-noise the sensor.

Author: Jake-The-Human
Repository: https://github.com/Jake-The-Human/Turntable-Tools
License: GPL-3.0-or-later (see LICENSE file for details)
Date Created: 2024-12-17

This file is part of Turntable Tools.

Turntable Tools is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Turntable Tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Turntable Tools. If not, see <https://www.gnu.org/licenses/>.
"""

_MOVING_AVG_SIZE: int = 10


def _get_next_index(index: int, list_len: int) -> int:
    """This is for the moving average index so it does not go out of bounds"""
    return (index + 1) % list_len


class MovingAvg:
    def __init__(self, size: int = _MOVING_AVG_SIZE):
        self._index = 0
        self._size = size
        self._buffer: list[float] = [0.0] * size

    def clear(self) -> None:
        """Resets avg"""
        self._index = 0
        self._buffer: list[float] = [0.0] * self._size

    def update(self, data: float) -> float:
        """update moving average and return the current avg"""
        # Replace the oldest data in the buffer
        self._buffer[self._index] = data
        self._index = _get_next_index(self._index, self._size)

        # Calculate the moving average
        return sum(self._buffer) / self._size


class MovingAvgTuple:
    def __init__(self, size: int = _MOVING_AVG_SIZE):
        self._index = 0
        self._size = size
        self._buffer: list[tuple] = [(0, 0, 0)] * size

    def clear(self) -> None:
        """Resets avg"""
        self._index = 0
        self._buffer: list[tuple] = [(0, 0, 0)] * self._size

    def update(self, data: tuple[float, float, float]) -> list:
        """update moving average and return the current avg"""
        # Replace the oldest data in the buffer
        self._buffer[self._index] = data
        self._index = _get_next_index(self._index, self._size)

        # Calculate the moving average
        return [
            sum(buffer_data) / len(buffer_data) for buffer_data in zip(*self._buffer)
        ]
