"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: about_screen.py
Description: This file is about the about page on the device.

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

from turntable_tools import colors as COLORS
from turntable_tools.helper import FONT


class AboutScreen(displayio.Group):
    """The about screen"""

    def __init__(self) -> None:
        super().__init__()
        _text_about = label.Label(
            FONT,
            text="Author: Jake Adamson\nMade in Boston MA B^)"
            "\nGitHub: Jake-The-\nHuman/Turntable-Tools",
            color=COLORS.DISPLAY_WHITE,
            x=2,
            y=8,
        )
        self.append(_text_about)
