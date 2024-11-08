import board
import displayio
import digitalio
import os

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

from adafruit_display_text import label
from adafruit_displayio_sh1107 import SH1107

import terminalio


DEVICE_ADDRESS=0x3C

WHITE = 0xFFFFFF
BLACK = 0x000000

class Screen:
    def __init__(self, i2c):
        self.button_c = digitalio.DigitalInOut(board.D5)
        self.button_c.switch_to_input(pull=digitalio.Pull.UP)
        self.button_b = digitalio.DigitalInOut(board.D6)
        self.button_b.switch_to_input(pull=digitalio.Pull.UP)
        self.button_a = digitalio.DigitalInOut(board.D9)
        self.button_a.switch_to_input(pull=digitalio.Pull.UP) 

        displayio.release_displays()

        # SH1107 is vertically oriented 64x128
        self._width  = int(os.getenv("CIRCUITPY_DISPLAY_WIDTH", 128))
        self._height = int(os.getenv("CIRCUITPY_DISPLAY_HEIGHT", 64))

        display_bus = I2CDisplayBus(i2c, device_address=DEVICE_ADDRESS)

        display = SH1107(
            display_bus, width=self._width, height=self._height
        )

        # Make the display context
        splash = displayio.Group()
        display.root_group = splash

        self.text_acceleration = label.Label(terminalio.FONT, text="", color=WHITE, x=8, y=8)
        splash.append(self.text_acceleration)

        self.text_gyro = label.Label(terminalio.FONT, text="", color=WHITE, x=8, y=16)
        splash.append(self.text_gyro)

        self.text_rpm = label.Label(terminalio.FONT, text="", color=WHITE, x=8, y=24)
        splash.append(self.text_rpm)

        self.text_degree = label.Label(terminalio.FONT, text="", color=WHITE, x=8, y=32)
        splash.append(self.text_degree)


    def width(self) -> int:
        return self._width
    
    def height(self) -> int:
        return self._height
    
    def checkButtons(self) -> tuple[bool, bool, bool]:
        return (not self.button_a.value, not self.button_b.value, not self.button_c.value)

    def display(self, acceleration: tuple[float, float, float], gyro: tuple[float, float, float], rpm: float, degree: float):
        self.text_acceleration.text = "X:%.2f,Y:%.2f,Z:%.2f m/s^2" % (acceleration)
        self.text_gyro.text = "X:%.2f,Y:%.2f,Z:%.2f radians/s" % (gyro)
        self.text_rpm.text = "RPM:%.2f" % (rpm)
        self.text_degree.text = "Degree:%.2f" % (degree)

