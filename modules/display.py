"""This file wraps the screen logic"""

import os
import board
import displayio
import digitalio

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

from adafruit_displayio_sh1107 import SH1107


DEVICE_ADDRESS = 0x3C


class Display:
    def __init__(self, i2c) -> None:
        self.button_c = digitalio.DigitalInOut(board.D5)
        self.button_c.switch_to_input(pull=digitalio.Pull.UP)
        self.button_b = digitalio.DigitalInOut(board.D6)
        self.button_b.switch_to_input(pull=digitalio.Pull.UP)
        self.button_a = digitalio.DigitalInOut(board.D9)
        self.button_a.switch_to_input(pull=digitalio.Pull.UP)

        displayio.release_displays()

        # SH1107 is vertically oriented 64x128
        self._width = int(os.getenv("CIRCUITPY_DISPLAY_WIDTH", "128"))
        self._height = int(os.getenv("CIRCUITPY_DISPLAY_HEIGHT", "64"))

        display_bus = I2CDisplayBus(i2c, device_address=DEVICE_ADDRESS)

        self.display = SH1107(display_bus, width=self._width, height=self._height)

    def width(self) -> int:
        """Return the width of the screen"""
        return self._width

    def height(self) -> int:
        """Returns the height of the screen"""
        return self._height

    def check_buttons(self) -> tuple[bool, bool, bool]:
        """checkes which button is pushed on the screen"""
        return not self.button_a.value, not self.button_b.value, not self.button_c.value

    def set_display(self, group: displayio.Group) -> None:
        if group != self.display.root_group:
            self.display.root_group = group
