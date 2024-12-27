"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: rumble_mode.py
Description: This is how rumble is measured.

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

import time
from neopixel import NeoPixel

from turntable_tools.sensors.mems_sensor import MemsSensor
from turntable_tools.buttons import Buttons
from turntable_tools.moving_average import MovingAvgTuple, MovingAvg
from turntable_tools import colors as COLORS
from turntable_tools.helper import (
    RUMBLE_TEST_START_UP_TIME,
    RUMBLE_TEST_LEN,
)

_TOTAL_TEST_LEN: float = RUMBLE_TEST_LEN + RUMBLE_TEST_START_UP_TIME


class RumbleMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self._moving_avg = MovingAvgTuple()
        self._avg_intensity = MovingAvg()
        self._time: float = 0

        self._record_data: bool = False
        self._start_up: bool = False
        self.result: tuple = (0, 0, 0, 0)

    def handle_buttons(self, buttons: Buttons) -> None:
        """Any mode specific action that are triggered by a button"""
        if buttons.b_pressed:
            self.start()

    def update(self, sensor: MemsSensor) -> None:
        """
        Rumble Intensity Calculation:
            The variable rumble_intensity is a simple measure of vibration strength,
            calculated as the deviation from the moving average
            (like the RMS value of recent changes).
        """
        # Finding the moving avg here to try and de-noise sensor
        avg_x, avg_y, avg_z = self._moving_avg.update(sensor.get_acceleration)

        x, y, z = sensor.get_acceleration
        intensity: float = (
            (x - avg_x) ** 2 + (y - avg_y) ** 2 + (z - avg_z) ** 2
        ) ** 0.5

        avg_rumble_intensity: float = self._avg_intensity.update(intensity)

        current_time: float = time.time() - self._time

        if RUMBLE_TEST_START_UP_TIME <= current_time <= _TOTAL_TEST_LEN:
            self._pixel.fill(COLORS.NEO_PIXEL_GREEN)
            self._record_data = True
            self._start_up = False

        elif self._record_data:
            self.stop()
            self.result = (avg_x, avg_y, avg_z, avg_rumble_intensity)

    @property
    def is_recording_data(self) -> bool:
        """Is used to check if we are capturing rpm data"""
        return self._record_data

    @property
    def is_starting_data(self) -> bool:
        """Is used to check if we are letting the turntable get upto speed"""
        return self._start_up

    def start(self) -> None:
        """Start recording data for the wow and flutter calc"""
        self._pixel.fill(COLORS.NEO_PIXEL_YELLOW)
        self._start_up = True
        self._time = time.time()

    def stop(self) -> None:
        """Stop recording data for the wow and flutter calc"""
        self._pixel.fill(COLORS.NEO_PIXEL_RED)
        self._record_data = False
        self._time = 0
