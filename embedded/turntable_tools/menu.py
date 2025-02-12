"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: menu.py
Description: This is how the menu is handled.

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

from displayio import Group
from adafruit_display_text import label
from turntable_tools import colors as COLORS
from turntable_tools.helper import FONT, CIRCUITPY_DISPLAY_WIDTH


class Menu:
    def __init__(
        self, items: list, visible_items: int = 1, x: int = 0, y: int = 0
    ) -> None:
        self._item_index: int = 0
        self._menu_index: int = 0
        self._prev_index: int = -1
        self.menu_items_names: list = items

        self.group = Group(x=x, y=y)
        self._menu_items: list[label.Label] = []
        for i in range(visible_items):
            new_item = label.Label(
                FONT,
                text=items[i][1],
                color=COLORS.DISPLAY_WHITE,
                padding_left=2,
                padding_right=CIRCUITPY_DISPLAY_WIDTH,
            )
            new_item.y = new_item.height * i
            self._menu_items.append(new_item)
            self.group.append(new_item)

        self._menu_items[self._menu_index].background_color = COLORS.DISPLAY_WHITE
        self._menu_items[self._menu_index].color = COLORS.DISPLAY_BLACK

    def __len__(self):
        return len(self._menu_items)

    def select(self) -> int:
        """Return the current index"""
        return self.menu_items_names[self._item_index][0]

    def up(self) -> None:
        """Move the menu index up"""
        self._prev_index = self._menu_index
        self._item_index = (self._item_index - 1) % len(self.menu_items_names)
        self._menu_index = (self._menu_index - 1) % len(self._menu_items)
        self._update()

    def down(self) -> None:
        """Move the menu index down"""
        self._prev_index = self._menu_index
        self._item_index = (self._item_index + 1) % len(self.menu_items_names)
        self._menu_index = (self._menu_index + 1) % len(self._menu_items)
        self._update()

    def get_item(self, index: int) -> label.Label:
        """Get menu item at that index"""
        return self._menu_items[index]

    def _update(self) -> None:
        """Redraws the list"""
        if not self._menu_items:
            return

        top_index: int = self._item_index
        bottom_index: int = top_index + len(self._menu_items)
        # if bottom_index <= len(self.menu_items_names):
        # this is where the menu gui text is updated
        for i, item in enumerate(range(top_index, bottom_index)):
            if item < len(self.menu_items_names):
                self._menu_items[i].text = self.menu_items_names[item][1]
            else:
                self._menu_items[i].text = ""
