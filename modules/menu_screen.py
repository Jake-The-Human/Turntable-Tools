"""This file draw the menu to the screen"""
from time import time
import displayio
from adafruit_display_text import label

from .display import Display
from .battery_status import BatteryStatus
from .menu import Menu
from .helper import (
    DisplayColor,
    STRINGS,
    Mode,
    FONT,
    CIRCUITPY_DISPLAY_WIDTH,
    HAS_BATTERY_STATUS_CIRCUIT,
    WHITE_PALETTE,
)


class MenuScreen:
    def __init__(self, battery_info, menu_items: list[int]) -> None:
        # Make the display context
        self._main_group = displayio.Group()

        # Temp Main Menu elements
        title_group = displayio.Group()
        text_title = label.Label(
            FONT, text=STRINGS.TITLE, color=DisplayColor.WHITE, y=8, padding_left=2
        )
        separator_bitmap = displayio.Bitmap(CIRCUITPY_DISPLAY_WIDTH, 1, 1)
        separator = displayio.TileGrid(
            separator_bitmap, pixel_shader=WHITE_PALETTE, y=14
        )

        menu_items_data = []
        for mode in menu_items:
            menu_items_data.append([mode, Mode.MODE_TO_STR[mode]])

        self._menu = Menu(items=menu_items_data, visible_items=4, x=2, y=22)

        title_group.append(text_title)

        if HAS_BATTERY_STATUS_CIRCUIT:
            self._battery_status = BatteryStatus(battery_info, CIRCUITPY_DISPLAY_WIDTH - 24, 4)
            title_group.append(self._battery_status.get_group())

        title_group.append(separator)
        self._main_group.append(title_group)
        self._main_group.append(self._menu.group)

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
        screen.set_display(self._main_group)

    def update(self) -> None:
        """Update the Menu screen"""
        if HAS_BATTERY_STATUS_CIRCUIT:
            self._battery_status.update()
