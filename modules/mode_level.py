class Leveling:
    def __init__(self) -> None:
        self._buffer_index: int = 0
        self._buffer_x: list[float] = [0, 0, 0]
        self._buffer_y: list[float] = [0, 0, 0]
        self._buffer_len = len(self._buffer_x)

    def _get_buffer_index(self) -> int:
        self._buffer_index = (self._buffer_index + 1) % self._buffer_len
        return self._buffer_index

    def update(self, x: float, y: float) -> tuple[float, float]:
        new_index = self._get_buffer_index()
        self._buffer_x[new_index] = x
        self._buffer_y[new_index] = y
        return (
            sum(self._buffer_x) / self._buffer_len,
            sum(self._buffer_y) / self._buffer_len,
        )
