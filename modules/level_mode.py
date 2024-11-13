"""Describes Leveling logic"""

from neopixel import NeoPixel

_MOVING_AVG_SIZE: int = 10


class LevelMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self._buffer_index: int = 0
        self._buffer_len: int = _MOVING_AVG_SIZE
        self._buffer_x: list[float] = [0 for _ in range(self._buffer_len)]
        self._buffer_y: list[float] = [0 for _ in range(self._buffer_len)]

    def _get_buffer_index(self) -> int:
        """This is for the moving average index so it does not go out of bounds"""
        self._buffer_index = (self._buffer_index + 1) % self._buffer_len
        return self._buffer_index

    def update(self, sensor_data: tuple[float, float, float]) -> tuple[float, float]:
        """This returns normalized x and y values"""
        new_index = self._get_buffer_index()
        x, y, _ = sensor_data
        self._buffer_x[new_index] = x
        self._buffer_y[new_index] = y
        return (
            sum(self._buffer_x) / self._buffer_len,
            sum(self._buffer_y) / self._buffer_len,
        )
