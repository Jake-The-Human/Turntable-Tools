"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: level_screen.py
Description: This is were we draw the level info to the screen.

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
from vectorio import Polygon
from adafruit_display_text import label

from turntable_tools.modes.level_mode import LevelMode
from turntable_tools import colors as COLORS
from turntable_tools import strings as STRINGS
from turntable_tools.helper import (
    FONT,
    CIRCUITPY_DISPLAY_WIDTH,
    CIRCUITPY_DISPLAY_HEIGHT,
    SHOW_X_Y,
)

_NORTH = 0
_EAST = 1
_SOUTH = 2
_WEST = 3


class LevelScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()

        BORDER: int = 2
        # Box that show the status of the leveling
        box_width: int = CIRCUITPY_DISPLAY_WIDTH // 2
        box_height: int = CIRCUITPY_DISPLAY_HEIGHT // 2
        color_bitmap = displayio.Bitmap(box_width, box_height, 1)

        bg_sprite = displayio.TileGrid(
            color_bitmap,
            pixel_shader=COLORS.PALETTE_WHITE,
            x=box_width - (box_width // 2),
            y=box_height - (box_height // 2),
        )

        inner_bitmap = displayio.Bitmap(box_width - BORDER, box_height - BORDER, 1)

        inner_sprite = displayio.TileGrid(
            inner_bitmap,
            pixel_shader=COLORS.PALETTE_BLACK,
            x=bg_sprite.x + 1,
            y=bg_sprite.y + 1,
        )

        # Some triangles to help move you in the right direction
        top_left: tuple[int, int] = (inner_sprite.x, inner_sprite.y)
        top_right: tuple[int, int] = (inner_sprite.x + box_width, inner_sprite.y)
        center_point: tuple[int, int] = (
            inner_sprite.x + (box_width // 2),
            inner_sprite.y + (box_height // 2),
        )
        bottom_left: tuple[int, int] = (inner_sprite.x, inner_sprite.y + box_height)
        bottom_right: tuple[int, int] = (
            inner_sprite.x + box_width,
            inner_sprite.y + box_height,
        )

        triangle_points: list[list[tuple[int, int]]] = [
            [top_left, center_point, top_right],
            [top_right, center_point, bottom_right],
            [bottom_left, center_point, bottom_right],
            [top_left, center_point, bottom_left],
        ]

        self._triangles: list[Polygon] = [
            Polygon(pixel_shader=COLORS.PALETTE_WHITE, points=triangle, x=0, y=0)
            for triangle in triangle_points
        ]

        # The raw x and y value from the sensor
        self._text_level_x_y = label.Label(
            FONT,
            color=COLORS.DISPLAY_WHITE,
            background_color=COLORS.DISPLAY_BLACK,
            padding_left=1,
            x=BORDER + 1,
            y=8 + 1,
        )

        # if you can read this then you are good to go!
        text_leveled = label.Label(
            FONT, text=STRINGS.LEVEL, color=COLORS.DISPLAY_BLACK, scale=2
        )
        text_leveled.x = (
            inner_sprite.x + ((box_width // 2) - text_leveled.width) + BORDER
        )
        text_leveled.y = inner_sprite.y + (box_height // 2)

        self.append(bg_sprite)
        self.append(inner_sprite)

        for triangle in self._triangles:
            triangle.hidden = True
            self.append(triangle)

        if SHOW_X_Y:
            self.append(self._text_level_x_y)

        self.append(text_leveled)

    def update(self, level_mode: LevelMode) -> None:
        """This update the x and y values on the display"""
        x, y = level_mode.current_position
        if SHOW_X_Y:
            self._text_level_x_y.text = f"X:{x:.2f} Y:{y:.2f}"
        x_rounded: float = round(x, 1)
        y_rounded: float = round(y, 1)
        self._triangles[_NORTH].hidden = y_rounded > 0
        self._triangles[_EAST].hidden = x_rounded < 0
        self._triangles[_SOUTH].hidden = y_rounded < 0
        self._triangles[_WEST].hidden = x_rounded > 0
