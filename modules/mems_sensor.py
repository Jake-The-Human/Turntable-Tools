"""Mems sensor data capture happens here"""

from math import pi
from busio import I2C
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

from .moving_average import MovingAvgTuple


class MemsSensor:
    def __init__(self, i2c: I2C):
        self._sensor = LSM6DS3(i2c)

        self.acceleration: tuple[float, float, float] = (0, 0, 0)
        self.gyro: tuple[float, float, float] = (0, 0, 0)
        self._sensor_temp: float = 0.0

        self.avg_accel = MovingAvgTuple()
        self.avg_gyro = MovingAvgTuple()

        self.acceleration_offset: tuple[float, float, float] = (0, 0, 0)
        self.gyro_offset: tuple[float, float, float] = (0, 0, 0)

    def update(self) -> None:
        """Update the sensor position"""
        self.acceleration = self.avg_accel.update(self._sensor.acceleration)
        self.gyro = self.avg_gyro.update(self._sensor.gyro)
        self._sensor_temp = self._sensor.temperature

    def clear(self) -> None:
        """Resets member data to help make new measurements better"""
        self.acceleration = (0, 0, 0)
        self.gyro = (0, 0, 0)
        self._sensor_temp = 0.0

        self.avg_accel.clear()
        self.avg_gyro.clear()

        self.acceleration_offset = (0, 0, 0)
        self.gyro_offset = (0, 0, 0)

    @property
    def get_acceleration(self) -> tuple[float, float, float]:
        """Gets the acceleration data"""
        acc_x, acc_y, acc_z = self.acceleration
        offset_x, offset_y, offset_z = self.acceleration_offset
        return (acc_x - offset_x, acc_y - offset_y, acc_z - offset_z)

    @property
    def get_gyro(self) -> tuple[float, float, float]:
        """Gets the gyro data"""
        gyro_x, gyro_y, gyro_z = self.gyro
        offset_x, offset_y, offset_z = self.gyro_offset
        return (gyro_x - offset_x, gyro_y - offset_y, gyro_z - offset_z)

    @property
    def get_rpm(self) -> float:
        """gets RPM from gyro"""
        _, _, gyro_z = self.get_gyro
        return abs(gyro_z * 60.0 / (2.0 * pi))

    @property
    def get_degrees(self) -> float:
        """gets degrees from gyro"""
        _, _, gyro_z = self.get_gyro
        return gyro_z * (180.0 / pi)

    def set_offsets(
        self,
        acceleration_offset: tuple[float, float, float],
        gyro_offset: tuple[float, float, float],
    ) -> None:
        """Update the offset of the sensor"""
        self.acceleration_offset = acceleration_offset
        self.gyro_offset = gyro_offset
