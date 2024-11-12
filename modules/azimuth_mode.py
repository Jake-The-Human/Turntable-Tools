"""Describes Azimuth logic"""

from neopixel import NeoPixel


class AzimuthMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel

    def update(self) -> None:
        pass
