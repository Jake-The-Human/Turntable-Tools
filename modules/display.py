"""This file wraps the screen logic"""

import board
import displayio
import digitalio

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

from adafruit_displayio_sh1107 import SH1107

from .helper import CIRCUITPY_DISPLAY_WIDTH, CIRCUITPY_DISPLAY_HEIGHT


DEVICE_ADDRESS = 0x3C


class Display:
    def __init__(self, i2c) -> None:
        self._button_c = digitalio.DigitalInOut(board.D5)
        self._button_c.switch_to_input(pull=digitalio.Pull.UP)
        self._button_b = digitalio.DigitalInOut(board.D6)
        self._button_b.switch_to_input(pull=digitalio.Pull.UP)
        self._button_a = digitalio.DigitalInOut(board.D9)
        self._button_a.switch_to_input(pull=digitalio.Pull.UP)

        displayio.release_displays()

        self._width: int = CIRCUITPY_DISPLAY_WIDTH
        self._height: int = CIRCUITPY_DISPLAY_HEIGHT

        display_bus = I2CDisplayBus(i2c, device_address=DEVICE_ADDRESS)
        self._display = SH1107(display_bus, width=self._width, height=self._height)

    def check_buttons(self) -> tuple[bool, bool, bool]:
        """checks which button is pushed on the screen"""
        return not self._button_a.value, not self._button_b.value, not self._button_c.value

    def set_display(self, group: displayio.Group) -> None:
        """This function tells the display which group to show"""
        if group != self._display.root_group:
            self._display.root_group = group
