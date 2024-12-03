"""This file is the moving avg logic that is used to de-noise the sensor"""

_MOVING_AVG_SIZE: int = 10


def _get_next_index(index: int, list_len: int) -> int:
    """This is for the moving average index so it does not go out of bounds"""
    return (index + 1) % list_len


class MovingAvg:
    def __init__(self, size: int = _MOVING_AVG_SIZE):
        self._index = 0
        self._size = size
        self._buffer: list[float] = [0.0] * size

    def update(self, data: float) -> float:
        """update moving average and return the current avg"""
        # Replace the oldest data in the buffer
        self._buffer[self._index] = data
        self._index = _get_next_index(self._index, self._size)

        # Calculate the moving average
        return sum(self._buffer) / self._size


class MovingAvgTuple:
    def __init__(self, size: int = _MOVING_AVG_SIZE):
        self._index = 0
        self._size = size
        self._buffer: list[tuple] = [(0, 0, 0)] * size

    def update(self, data: tuple[float, float, float]) -> list:
        """update moving average and return the current avg"""
        # Replace the oldest data in the buffer
        self._buffer[self._index] = data
        self._index = _get_next_index(self._index, self._size)

        # Calculate the moving average
        return [
            sum(buffer_data) / len(buffer_data) for buffer_data in zip(*self._buffer)
        ]
