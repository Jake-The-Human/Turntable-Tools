from math import pi
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

def _low_pass_filter(previous_value:float, current_value:float, alpha:float=0.5):
    """
    Simple low-pass filter
    :param previous_value: The last filtered value
    :param current_value: The current sensor reading
    :param alpha: Smoothing factor (0 < alpha < 1)
    :return: Filtered value
    """
    return alpha * current_value + (1 - alpha) * previous_value

class MemsSensor:
    def __init__(self, i2c):
        self._sensor = LSM6DS3(i2c)
        self._prev_acceleration = (0, 0, 0)
        self._prev_gyro = (0, 0, 0)
        self._acceleration_offset: tuple[float, float, float] = (0, 0, 0)
        self._gyro_offest: tuple[float, float, float] = (0, 0, 0)
    
    def _low_pass_tuple(self, prev_data: tuple, cur_data: tuple):
        return (_low_pass_filter(prev_data[0], cur_data[0]),
                _low_pass_filter(prev_data[1], cur_data[1]),
                _low_pass_filter(prev_data[2], cur_data[2]))

    def getAcceleration(self) -> tuple:
        self._prev_acceleration = self._low_pass_tuple(
            prev_data=self._prev_acceleration,
            cur_data=(self._sensor.acceleration[0] - self._acceleration_offset[0],
            self._sensor.acceleration[1] - self._acceleration_offset[1],
            self._sensor.acceleration[2] - self._acceleration_offset[2])
        )
        return self._prev_acceleration

    def getGyro(self) -> tuple:
        self._prev_gyro = self._low_pass_tuple(
            prev_data=self._prev_acceleration,
            cur_data=(self._sensor.gyro[0] - self._gyro_offest[0],
            self._sensor.gyro[1] - self._gyro_offest[1],
            self._sensor.gyro[2] - self._gyro_offest[2])
        )
        return self._prev_gyro
    
    def getRPM(self) -> float:
        return abs(self.getGyro()[2] * 60.0 / (2.0 * pi))
    
    def getDegrees(self) -> float:
        return self.getGyro()[2] * (180.0 / pi)
    
    def setOffset(self) -> None:
        self._acceleration_offset = self._sensor.acceleration
        self._gyro_offest = self._sensor.gyro
    