"""This file wraps the screen logic"""

import displayio

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

from adafruit_displayio_sh1107 import SH1107

from .helper import CIRCUITPY_DISPLAY_WIDTH, CIRCUITPY_DISPLAY_HEIGHT


_DEVICE_ADDRESS = 0x3C


class Display:
    def __init__(self, i2c) -> None:
        displayio.release_displays()
        display_bus = I2CDisplayBus(i2c, device_address=_DEVICE_ADDRESS)
        self._display = SH1107(
            display_bus,
            width=CIRCUITPY_DISPLAY_WIDTH,
            height=CIRCUITPY_DISPLAY_HEIGHT,
        )

    def set_display(self, group: displayio.Group) -> None:
        """This function tells the display which group to show"""
        if group != self._display.root_group:
            self._display.root_group = group
