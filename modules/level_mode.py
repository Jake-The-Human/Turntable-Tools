"""Describes Leveling logic"""

from neopixel import NeoPixel
from .moving_average import MovingAvgTuple


class LevelMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self._moving_avg = MovingAvgTuple()

    def update(self, sensor_data: tuple[float, float, float]) -> tuple[float, float]:
        """This returns normalized x and y values"""
        x, y, _ = self._moving_avg.update(sensor_data)
        return (x, y)
