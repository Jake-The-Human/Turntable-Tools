from math import pi
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3


class MemsSensor:
    def __init__(self, i2c):
        self._sensor = LSM6DS3(i2c)

        self._acceleration: tuple[float, float, float] = self._sensor.acceleration
        self._gyro: tuple[float, float, float] = self._sensor.gyro
        self.sensor_temp: float = self._sensor.temperature

        self._acceleration_offset: tuple[float, float, float] = (0, 0, 0)
        self._gyro_offest: tuple[float, float, float] = (0, 0, 0)

    def update(self) -> None:
        """Update the sensor position"""
        self._acceleration = self._sensor.acceleration
        self._gyro = self._sensor.gyro
        self.sensor_temp = self._sensor.temperature

    def get_acceleration(self) -> tuple[float, float, float]:
        """Gets the acceleration data"""
        acc_x, acc_y, acc_z = self._acceleration
        offset_x, offset_y, offset_z = self._acceleration_offset
        return (acc_x - offset_x, acc_y - offset_y, acc_z - offset_z)

    def get_gyro(self) -> tuple[float, float, float]:
        """Gets the gyro data"""
        gyro_x, gyro_y, gyro_z = self._gyro
        offset_x, offset_y, offset_z = self._gyro_offest

        return (gyro_x - offset_x, gyro_y - offset_y, gyro_z - offset_z)

    def get_rpm(self) -> float:
        _, _, gyro_z = self.get_gyro()
        return abs(gyro_z * 60.0 / (2.0 * pi))

    def get_degrees(self) -> float:
        _, _, gyro_z = self.get_gyro()
        return gyro_z * (180.0 / pi)

    def set_offset(self) -> None:
        self._acceleration_offset = self._sensor.acceleration
        self._gyro_offest = self._sensor.gyro

    def reset_offset(self) -> None:
        self._acceleration_offset = (0, 0, 0)
        self._gyro_offest = (0, 0, 0)
