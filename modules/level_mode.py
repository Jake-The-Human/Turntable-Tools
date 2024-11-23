"""Describes Leveling logic"""

from neopixel import NeoPixel
from .mems_sensor import MemsSensor
from .buttons import Buttons
from .helper import PixelColor


class LevelMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self.current_position: tuple = (0, 0)

    def handle_buttons(self, _: Buttons) -> None:
        pass

    def update(self, sensor: MemsSensor) -> None:
        """This returns normalized x and y values"""
        x, y, _ = sensor.get_acceleration()
        self.current_position = (x, y)
        if (x, y) == (0, 0):
            self._pixel.fill(PixelColor.GREEN)
        else:
            self._pixel.fill(PixelColor.OFF)
