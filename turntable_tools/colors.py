"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: colors.py
Description: This file holds all the colors.

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

from displayio import Palette

# Colors for the display
DISPLAY_BLACK: int = 0x000000
DISPLAY_WHITE: int = 0xFFFFFF


# Colors for NeoPixel
NEO_PIXEL_OFF: tuple = (0, 0, 0)
NEO_PIXEL_GREEN: tuple = (0, 255, 0)
NEO_PIXEL_YELLOW: tuple = (255, 255, 0)
NEO_PIXEL_RED: tuple = (255, 0, 0)


# Black and white color palettes
PALETTE_BLACK = Palette(1)
PALETTE_BLACK[0] = DISPLAY_BLACK
PALETTE_WHITE = Palette(1)
PALETTE_WHITE[0] = DISPLAY_WHITE
