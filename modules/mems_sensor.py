from math import pi
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

from .calibrate_mode import CalibrateMode


class MemsSensor:
    def __init__(self, i2c):
        self._sensor = LSM6DS3(i2c)

        self.calibrate_mode = CalibrateMode()

        self.acceleration: tuple[float, float, float] = (0, 0, 0)
        self.gyro: tuple[float, float, float] = (0, 0, 0)
        self._sensor_temp: float = 0.0

    def update(self) -> None:
        """Update the sensor position"""
        self.acceleration = self._sensor.acceleration
        self.gyro = self._sensor.gyro
        self._sensor_temp = self._sensor.temperature

    def get_acceleration(self) -> tuple[float, float, float]:
        """Gets the acceleration data"""
        acc_x, acc_y, acc_z = self.acceleration
        offset_x, offset_y, offset_z = self.calibrate_mode.acceleration_offset
        return (acc_x - offset_x, acc_y - offset_y, acc_z - offset_z)

    def get_gyro(self) -> tuple[float, float, float]:
        """Gets the gyro data"""
        gyro_x, gyro_y, gyro_z = self.gyro
        offset_x, offset_y, offset_z = self.calibrate_mode.gyro_offset

        return (gyro_x - offset_x, gyro_y - offset_y, gyro_z - offset_z)

    def get_rpm(self) -> float:
        """gets RPM from gyro"""
        _, _, gyro_z = self.get_gyro()
        return abs(gyro_z * 60.0 / (2.0 * pi))

    def get_degrees(self) -> float:
        """gets degrees from gyro"""
        _, _, gyro_z = self.get_gyro()
        return gyro_z * (180.0 / pi)
