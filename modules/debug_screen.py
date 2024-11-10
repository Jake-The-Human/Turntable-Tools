"""This is file describes how the debug the sensor info is displayed"""

import displayio
from adafruit_display_text import label

from .display import Display
from .mems_sensor import MemsSensor
from .helper import DisplayColor, FONT


class DebugScreen:
    def __init__(self) -> None:
        self.debug_group = displayio.Group()

        self.text_accel = label.Label(FONT, color=DisplayColor.WHITE, x=8, y=8)
        self.text_gyro = label.Label(FONT, color=DisplayColor.WHITE, x=8, y=18)
        self.text_rpm = label.Label(FONT, color=DisplayColor.WHITE, x=8, y=26)
        self.text_degree = label.Label(FONT, color=DisplayColor.WHITE, x=8, y=34)

        self.debug_group.append(self.text_accel)
        self.debug_group.append(self.text_gyro)
        self.debug_group.append(self.text_rpm)
        self.debug_group.append(self.text_degree)

    def update(self, sensor: MemsSensor) -> None:
        """This will draw raw sensor values to the screen"""
        acc_x, acc_y, acc_z = sensor.get_acceleration()
        gyro_x, gyro_y, gyro_z = sensor.get_gyro()
        rpm = sensor.get_rpm()
        degree = sensor.get_degrees()

        self.text_accel.text = f"X{acc_x:.2f},Y{acc_y:.2f},Z{acc_z:.2f} m/s^2"
        self.text_gyro.text = f"X:{gyro_x:.2f},Y:{gyro_y:.2f},Z:{gyro_z:.2f} radians/s"
        self.text_rpm.text = f"RPM:{rpm:.2f}"
        self.text_degree.text = f"Degree:{degree:.2f}"

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the debug info"""
        screen.set_display(self.debug_group)
