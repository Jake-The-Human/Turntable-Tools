"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: menu_screen.py
Description: This file draw the menu to the screen.

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

from turntable_tools.display import Display
from turntable_tools.battery_icon import BatteryIcon
from turntable_tools.menu import Menu
from turntable_tools import colors as COLORS
from turntable_tools import strings as STRINGS
from turntable_tools import mode_types as MODE
from turntable_tools.helper import (
    FONT,
    CIRCUITPY_DISPLAY_WIDTH,
    HAS_BATTERY_STATUS_CIRCUIT,
)


class MenuScreen(displayio.Group):
    def __init__(self, battery_info, menu_items: list[int]) -> None:
        super().__init__()

        text_title = label.Label(
            FONT, text=STRINGS.TITLE, color=COLORS.DISPLAY_WHITE, y=8, padding_left=2
        )
        separator_bitmap = displayio.Bitmap(CIRCUITPY_DISPLAY_WIDTH, 1, 1)
        separator = displayio.TileGrid(
            separator_bitmap, pixel_shader=COLORS.PALETTE_WHITE, y=14
        )

        menu_items_data = []
        for mode in menu_items:
            menu_items_data.append([mode, MODE.MODE_TO_STR[mode]])

        self._menu = Menu(items=menu_items_data, visible_items=4, x=2, y=22)

        self.append(text_title)

        if HAS_BATTERY_STATUS_CIRCUIT:
            self._battery_status = BatteryIcon(
                battery_info, CIRCUITPY_DISPLAY_WIDTH - 24, 4
            )
            self.append(self._battery_status)

        self.append(separator)
        self.append(self._menu.group)

    def select(self) -> int:
        """Return the current index"""
        return self._menu.select()

    def up(self) -> int:
        """Move the menu index up"""
        return self._menu.up()

    def down(self) -> int:
        """Move the menu index down"""
        return self._menu.down()

    def show_screen(self, screen: Display) -> None:
        """This will make the display show main menu"""
        screen.set_display(self)

    def update(self) -> None:
        """Update the Menu screen"""
        if HAS_BATTERY_STATUS_CIRCUIT:
            self._battery_status.update()
