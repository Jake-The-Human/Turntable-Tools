"""Describes Leveling logic"""

from neopixel import NeoPixel

from turntable_tools.sensors.mems_sensor import MemsSensor
from turntable_tools.buttons import Buttons
from turntable_tools import colors as COLORS


class LevelMode:
    """This class is the logic to help level you turntable"""

    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self.current_position: tuple = (0, 0)

    def handle_buttons(self, _: Buttons) -> None:
        """Not used"""
        return

    def update(self, sensor: MemsSensor) -> None:
        """This returns normalized x and y values"""
        x, y, _ = sensor.get_acceleration
        self.current_position = (x, y)
        if (x, y) == (0, 0):
            self._pixel.fill(COLORS.NEO_PIXEL_GREEN)
        else:
            self._pixel.fill(COLORS.NEO_PIXEL_OFF)
