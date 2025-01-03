"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: display.py
Description: This file wraps the screen logic.

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

from displayio import release_displays, Group
from adafruit_displayio_sh1107 import SH1107

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

from .helper import DISPLAY_ADDRESS, CIRCUITPY_DISPLAY_WIDTH, CIRCUITPY_DISPLAY_HEIGHT


class Display:
    """This class is used to set up the hw display"""

    def __init__(self, i2c) -> None:
        release_displays()
        self.display = SH1107(
            bus=I2CDisplayBus(i2c_bus=i2c, device_address=DISPLAY_ADDRESS),
            width=CIRCUITPY_DISPLAY_WIDTH,
            height=CIRCUITPY_DISPLAY_HEIGHT,
        )

    def set_display(self, group: Group) -> None:
        """This function tells the display which group to show"""
        if group != self.display.root_group:
            self.display.root_group = group
