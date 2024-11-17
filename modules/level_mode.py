"""Describes Leveling logic"""

from neopixel import NeoPixel
from .mems_sensor import MemsSensor
from .buttons import Buttons
from .moving_average import MovingAvgTuple


class LevelMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel: NeoPixel = pixel
        self._moving_avg = MovingAvgTuple()
        self.current_position: tuple = (0, 0)

    def handle_buttons(self, _: Buttons) -> None:
        pass

    def update(self, sensor: MemsSensor) -> None:
        """This returns normalized x and y values"""
        x, y, _ = self._moving_avg.update(sensor.get_acceleration())
        self.current_position = (x, y)
