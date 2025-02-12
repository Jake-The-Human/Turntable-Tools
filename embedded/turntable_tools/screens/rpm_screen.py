"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: rpm_screen.py
Description: This file handles draw rpm data to the screen.

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

from turntable_tools.modes.rpm_mode import RPMMode
from turntable_tools import colors as COLORS
from turntable_tools import strings as STRINGS
from turntable_tools.helper import FONT


class RPMScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()
        self._text_rpm = label.Label(FONT, color=COLORS.DISPLAY_WHITE, scale=3, y=16)
        text_rpm_unit = label.Label(
            FONT, text=STRINGS.RPM, color=COLORS.DISPLAY_WHITE, scale=2, x=89, y=16
        )
        self._text_progress = label.Label(
            FONT, color=COLORS.DISPLAY_WHITE, scale=2, y=42
        )

        self._result_group = displayio.Group()
        self._text_avg = label.Label(FONT, color=COLORS.DISPLAY_WHITE, y=36)
        self._text_min_max = label.Label(FONT, color=COLORS.DISPLAY_WHITE, y=46)
        self._text_wow = label.Label(FONT, color=COLORS.DISPLAY_WHITE, y=56)

        self._result_group.append(self._text_avg)
        self._result_group.append(self._text_min_max)
        self._result_group.append(self._text_wow)

        self.append(self._text_rpm)
        self.append(text_rpm_unit)
        self.append(self._text_progress)
        self.append(self._result_group)

    def update(self, rpm_mode: RPMMode) -> None:
        """Update the RPM number on screen"""
        if rpm_mode.is_recording_data:
            self._text_progress.text = STRINGS.MEASURING

        elif rpm_mode.is_starting_data:
            self._text_progress.hidden = False
            self._result_group.hidden = True
            self._text_progress.text = STRINGS.START_TURNTABLE

        elif not rpm_mode.is_recording_data:
            avg_rpm, min_rpm, max_rpm, wow, flutter = rpm_mode.result
            self._text_progress.hidden = True
            self._result_group.hidden = False

            self._text_avg.text = f"{STRINGS.AVG}: {avg_rpm:.2f}"
            self._text_min_max.text = (
                f"{STRINGS.MIN}: {min_rpm:.2f} {STRINGS.MAX}: {max_rpm:.2f}"
            )
            self._text_wow.text = (
                f"{STRINGS.WOW_AND_FLUTTER}: {wow:.2f}% {flutter:.2f}%"
            )

        self._text_rpm.text = f"{rpm_mode.current_rpm:.2f}"
