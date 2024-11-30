"""This file wraps the screen logic"""

from displayio import release_displays, Group
from adafruit_displayio_sh1107 import SH1107

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

from .helper import DISPLAY_ADDRESS, CIRCUITPY_DISPLAY_WIDTH, CIRCUITPY_DISPLAY_HEIGHT


class Display:
    def __init__(self, i2c) -> None:
        release_displays()
        self.display = SH1107(
            bus=I2CDisplayBus(i2c_bus=i2c, device_address=DISPLAY_ADDRESS),
            width=CIRCUITPY_DISPLAY_WIDTH,
            height=CIRCUITPY_DISPLAY_HEIGHT,
        )

    def set_display(self, group: Group) -> None:
        """This function tells the display which group to show"""
        if group != self.display.root_group:
            self.display.root_group = group
