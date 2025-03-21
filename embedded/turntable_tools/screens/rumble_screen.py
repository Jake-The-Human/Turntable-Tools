"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: rumble_screen.py
Description: This file handles draw rumble data to the screen.

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

from math import log
import displayio
from adafruit_display_text import label

from turntable_tools.modes.rumble_mode import RumbleMode
from turntable_tools import colors as COLORS
from turntable_tools import strings as STRINGS
from turntable_tools.helper import FONT


_INTENSITY_INDEX: int = 0
_AVG_X_INDEX: int = 1
_AVG_Y_INDEX: int = 2
_AVG_Z_INDEX: int = 3


def _acceleration_to_db(accel_value: float, a_ref: float = 9.81) -> float:
    """Convert acceleration to decibels (relative to a_ref)."""
    return (
        20.0 * log(abs(accel_value) / a_ref, 10) if accel_value != 0 else -float("inf")
    )


class RumbleScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()
        self._text_progress = label.Label(
            FONT, color=COLORS.DISPLAY_WHITE, scale=2, y=28
        )

        self._result_group = displayio.Group()
        self._rumble_data: list = []
        number_of_data_points_to_display: int = 4
        for i in range(number_of_data_points_to_display):
            self._rumble_data.append(
                label.Label(FONT, text=" ", color=COLORS.DISPLAY_WHITE, padding_left=1)
            )
            self._rumble_data[i].x = 1
            self._rumble_data[i].y = 8 + (self._rumble_data[i].height * i)
            self._result_group.append(self._rumble_data[i])

        self.append(self._text_progress)
        self.append(self._result_group)

    def update(self, rumble_mode: RumbleMode) -> None:
        """Update the rumble number on screen"""
        if rumble_mode.is_recording_data:
            self._text_progress.text = STRINGS.MEASURING

        elif rumble_mode.is_starting_data:
            self._text_progress.hidden = False
            self._result_group.hidden = True
            self._text_progress.text = STRINGS.START_TURNTABLE

        elif not rumble_mode.is_recording_data:
            self._text_progress.hidden = True
            self._result_group.hidden = False
            avg_x, avg_y, avg_z, rumble_intensity = rumble_mode.result
            self._rumble_data[_INTENSITY_INDEX].text = (
                f"{STRINGS.INTENSITY}: {_acceleration_to_db(rumble_intensity):.2f}dB"
            )
            self._rumble_data[_AVG_X_INDEX].text = (
                f"Avg X: {_acceleration_to_db(avg_x):.2f}dB"
            )
            self._rumble_data[_AVG_Y_INDEX].text = (
                f"Avg Y: {_acceleration_to_db(avg_y):.2f}dB"
            )
            self._rumble_data[_AVG_Z_INDEX].text = (
                f"Avg Z: {_acceleration_to_db(avg_z):.2f}db"
            )
