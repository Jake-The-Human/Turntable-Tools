import time
from neopixel import NeoPixel

from .helper import PixelColor, RUMBLE_TEST_START_UP_TIME, RUMBLE_TEST_LEN

_MOVING_AVG_SIZE: int = 10
_TOTAL_TEST_LEN = RUMBLE_TEST_LEN + RUMBLE_TEST_START_UP_TIME


class RumbleMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self._buffer_index: int = 0
        self._buffer_len: int = _MOVING_AVG_SIZE
        self._buffer_x: list[float] = [0 for _ in range(self._buffer_len)]
        self._buffer_y: list[float] = [0 for _ in range(self._buffer_len)]
        self._buffer_z: list[float] = [0 for _ in range(self._buffer_len)]

        self._intensity_data: list[float] = []
        self._avg_x_data: list[float] = []
        self._avg_y_data: list[float] = []
        self._avg_z_data: list[float] = []
        self._record_data: bool = False
        self._start_up: bool = False
        self._time: float = 0
        self._result: tuple = (0, 0, 0, 0)

    def _get_buffer_index(self) -> int:
        """This is for the moving average index so it does not go out of bounds"""
        self._buffer_index = (self._buffer_index + 1) % self._buffer_len
        return self._buffer_index

    def get_results(self) -> tuple[float, float, float, float]:
        return self._result

    def update(
        self, sensor_data: tuple[float, float, float]
    ) -> tuple[float, float, float, float]:
        """
        Rumble Intensity Calculation:
            The variable rumble_intensity is a simple measure of vibration strength,
            calculated as the deviation from the moving average
            (like the RMS value of recent changes).
        """
        new_index = self._get_buffer_index()
        x, y, z = sensor_data
        self._buffer_x[new_index] = x
        self._buffer_y[new_index] = y
        self._buffer_z[new_index] = z
        # Finding the moving avg here to try and de-noise sensor
        avg_x: float = sum(self._buffer_x) / self._buffer_len
        avg_y: float = sum(self._buffer_y) / self._buffer_len
        avg_z: float = sum(self._buffer_z) / self._buffer_len

        rumble_intensity: float = (
            (x - avg_x) ** 2 + (y - avg_y) ** 2 + (z - avg_z) ** 2
        ) ** 0.5

        current_time = time.time() - self._time
        if current_time > RUMBLE_TEST_START_UP_TIME and current_time <= _TOTAL_TEST_LEN:
            self._pixel.fill(PixelColor.GREEN)
            self._record_data = True
            self._start_up = False
            self._intensity_data.append(rumble_intensity)
            self._avg_x_data.append(avg_x)
            self._avg_y_data.append(avg_y)
            self._avg_z_data.append(avg_z)
        elif self._record_data:
            self.stop()
            self._result = (
                sum(self._avg_x_data) / len(self._avg_x_data),
                sum(self._avg_y_data) / len(self._avg_y_data),
                sum(self._avg_z_data) / len(self._avg_z_data),
                sum(self._intensity_data) / len(self._intensity_data),
            )
            self._intensity_data.clear()
            self._avg_x_data.clear()
            self._avg_y_data.clear()
            self._avg_y_data.clear()

        return avg_x, avg_y, avg_z, rumble_intensity

    def is_recording_data(self) -> bool:
        """Is used to check if we are capturing rpm data"""
        return self._record_data

    def is_starting_data(self) -> bool:
        """Is used to check if we are letting the turntable get upto speed"""
        return self._start_up

    def start(self) -> None:
        """Start recording data for the wow and flutter calc"""
        self._pixel.fill(PixelColor.YELLOW)
        self._start_up = True
        self._time = time.time()

    def stop(self) -> None:
        """Stop recording data for the wow and flutter calc"""
        self._pixel.fill(PixelColor.RED)
        self._record_data = False
        self._time = 0
