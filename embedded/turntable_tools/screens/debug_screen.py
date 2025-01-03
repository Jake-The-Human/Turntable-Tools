"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: debug_screen.py
Description: This is file describes how the debug the sensor info is displayed.

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

import displayio
from adafruit_display_text import label

from turntable_tools.sensors.mems_sensor import MemsSensor
from turntable_tools import colors as COLORS
from turntable_tools.helper import FONT


class DebugScreen(displayio.Group):
    """This class can be used to debug the mems sensor"""
    def __init__(self) -> None:
        super().__init__()

        self.text_accel = label.Label(FONT, color=COLORS.DISPLAY_WHITE, x=8, y=8)
        self.text_gyro = label.Label(FONT, color=COLORS.DISPLAY_WHITE, x=8, y=18)
        self.text_rpm = label.Label(FONT, color=COLORS.DISPLAY_WHITE, x=8, y=26)
        self.text_degree = label.Label(FONT, color=COLORS.DISPLAY_WHITE, x=8, y=34)

        self.append(self.text_accel)
        self.append(self.text_gyro)
        self.append(self.text_rpm)
        self.append(self.text_degree)

    def update(self, sensor: MemsSensor) -> None:
        """This will draw raw sensor values to the screen"""
        acc_x, acc_y, acc_z = sensor.get_acceleration()
        gyro_x, gyro_y, gyro_z = sensor.get_gyro()
        rpm = sensor.get_rpm()
        degree = sensor.get_degrees()

        self.text_accel.text = f"X{acc_x:.2f},Y{acc_y:.2f},Z{acc_z:.2f} m/s^2"
        self.text_gyro.text = f"X:{gyro_x:.2f},Y:{gyro_y:.2f},Z:{gyro_z:.2f} radians/s"
        self.text_rpm.text = f"RPM:{rpm:.2f}"
        self.text_degree.text = f"Degree:{degree:.2f}"
