import time
from neopixel import NeoPixel
from .mems_sensor import MemsSensor
from .buttons import Buttons
from .helper import (
    HAS_SD_CARD,
    CALIBRATION_TEST_LEN,
    CALIBRATION_TEST_START_UP_TIME,
    PixelColor,
)
from .moving_average import MovingAvgTuple

_FILE_NAME = "calibration.txt"
_TOTAL_TEST_LEN = CALIBRATION_TEST_LEN + CALIBRATION_TEST_START_UP_TIME


def _write_to_file(
    acceleration_offset: tuple[float, float, float],
    gyro_offset: tuple[float, float, float],
) -> None:
    """Writes offset data to file for future use"""
    with open(f"/sd/{_FILE_NAME}", mode="w", encoding="ascii") as rpm_result:
        accel_x, accel_y, accel_z = acceleration_offset
        gyro_x, gyro_y, gyro_z = gyro_offset
        rpm_result.write(f"{accel_x} {accel_y} {accel_z}\n{gyro_x} {gyro_y} {gyro_z}")


def _read_to_file() -> list[tuple[float, float, float]]:
    acceleration_offset: tuple[float, float, float] = (0, 0, 0)
    gyro_offset: tuple[float, float, float] = (0, 0, 0)
    try:
        with open(f"/sd/{_FILE_NAME}", mode="r", encoding="ascii") as rpm_result:
            calibration_str: list[str] = rpm_result.read().split("\n")

            acceleration_offset = tuple(
                float(data) for data in calibration_str[0].split(" ")
            )
            gyro_offset = tuple(float(data) for data in calibration_str[1].split(" "))

    except Exception:
        print("Calibration file not found.")

    return [acceleration_offset, gyro_offset]


class CalibrateMemsMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self.acceleration_offset: tuple[float, float, float] = (0, 0, 0)
        self.gyro_offset: tuple[float, float, float] = (0, 0, 0)
        self._moving_avg_accel = MovingAvgTuple(21)
        self._moving_avg_gyro = MovingAvgTuple(21)

        self._record_data: bool = False
        self._start_up: bool = False
        self._time: float = 0

        if HAS_SD_CARD:
            self.acceleration_offset, self.gyro_offset = _read_to_file()

    def handle_buttons(self, buttons: Buttons) -> None:
        """Any mode specific action that are triggered by a button"""
        if buttons.b_pressed():
            self.start()

    def update(self, sensor: MemsSensor) -> None:
        """Writes the calibration data to a file for future use"""
        current_time: float = time.time() - self._time
        if (
            current_time > CALIBRATION_TEST_START_UP_TIME
            and current_time <= _TOTAL_TEST_LEN
        ):
            self._pixel.fill(PixelColor.GREEN)
            self._record_data = True
            self._start_up = False

            self.acceleration_offset = self._moving_avg_accel.update(
                sensor.acceleration
            )
            self.gyro_offset = self._moving_avg_gyro.update(sensor.gyro)

        elif self._record_data:
            self.stop()
            sensor.set_offsets(self.acceleration_offset, self.gyro_offset)
            if HAS_SD_CARD:
                _write_to_file(self.acceleration_offset, self.gyro_offset)

    def is_recording_data(self) -> bool:
        """Is used to check if we are capturing after button has been released"""
        return self._record_data

    def is_starting_data(self) -> bool:
        """Allows time for the button to be released"""
        return self._start_up

    def start(self) -> None:
        """Start recording data"""
        self._pixel.fill(PixelColor.YELLOW)
        self._start_up = True
        self._time = time.time()
        self.acceleration_offset = (0, 0, 0)
        self.gyro_offset = (0, 0, 0)

    def stop(self) -> None:
        """Stop recording data"""
        self._pixel.fill(PixelColor.RED)
        self._record_data = False
        self._time = 0
