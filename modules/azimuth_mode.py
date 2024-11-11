"""Describes Azimuth logic"""

from neopixel import NeoPixel

MOVING_AVG_SIZE: int = 10


class AzimuthMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self._buffer_index: int = 0
        self._buffer_len: int = MOVING_AVG_SIZE

    def _get_buffer_index(self) -> int:
        """This is for the moving average index so it does not go out of bounds"""
        self._buffer_index = (self._buffer_index + 1) % self._buffer_len
        return self._buffer_index

    def update(self) -> None:
        pass
