"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: azimuth_screen.py
Description: Draw the azimuth results.

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
from turntable_tools.modes.azimuth_mode import AzimuthMode
from turntable_tools import colors as COLORS
from turntable_tools import strings as STRINGS
from turntable_tools.helper import FONT


class AzimuthScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()

        self._crosstalk_text = label.Label(
            FONT,
            color=COLORS.DISPLAY_WHITE,
            background_color=COLORS.DISPLAY_BLACK,
            padding_left=1,
            x=0,
            y=8,
        )

        self._crosstalk_value_text = label.Label(
            FONT,
            color=COLORS.DISPLAY_WHITE,
            background_color=COLORS.DISPLAY_BLACK,
            padding_left=1,
            x=0,
            y=20,
        )

        self.append(self._crosstalk_text)
        self.append(self._crosstalk_value_text)

    def update(self, azimuth_mode: AzimuthMode) -> None:
        """Update the rms voltage and crosstalk"""

        if azimuth_mode.crosstalk_left < 0.0:
            channel: str = "L"
            rms: float = azimuth_mode.rms_left
            crosstalk: float = azimuth_mode.crosstalk_left
        else:
            channel: str = "R"
            rms: float = azimuth_mode.rms_right
            crosstalk: float = azimuth_mode.crosstalk_right

        self._crosstalk_text.text = (
            f"{STRINGS.ALIGNMENT}: {AzimuthScreen._alignment(crosstalk)}."
        )

        self._crosstalk_value_text.text = f"{channel}: {rms:.2f}mV, {crosstalk:.2f}dB"

    @staticmethod
    def _alignment(crosstalk_db: float) -> str:
        quality: str = STRINGS.POOR
        if crosstalk_db < -30.0:
            quality = STRINGS.EXCELLENT
        elif crosstalk_db < -25.0:
            quality = STRINGS.GREAT
        elif crosstalk_db < -20.0:
            quality = STRINGS.GOOD

        return quality
