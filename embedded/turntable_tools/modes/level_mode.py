"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: level_mode.py
Description: This is how level is measured.

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

from neopixel import NeoPixel

from turntable_tools.sensors.mems_sensor import MemsSensor
from turntable_tools.buttons import Buttons
from turntable_tools import colors as COLORS


class LevelMode:
    """This class is the logic to help level you turntable"""

    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self.current_position: tuple = (0, 0)

    def handle_buttons(self, _: Buttons) -> None:
        """Not used"""
        return

    def update(self, sensor: MemsSensor) -> None:
        """This returns normalized x and y values"""
        x, y, _ = sensor.get_acceleration
        self.current_position = (x, y)
        if (x, y) == (0, 0):
            self._pixel.fill(COLORS.NEO_PIXEL_GREEN)
        else:
            self._pixel.fill(COLORS.NEO_PIXEL_OFF)
