"""This file wraps the screen logic"""

import os
import board
import displayio
import digitalio

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

from adafruit_display_text import label
from adafruit_displayio_sh1107 import SH1107

import terminalio

from .mems_sensor import MemsSensor

from .screen_rpm import RPMScreen
from .screen_level import LevelingScreen
from .screen_main import MainScreen
import modules.modes as Mode


DEVICE_ADDRESS = 0x3C

WHITE = 0xFFFFFF
BLACK = 0x000000

RPM = "RPM, Wow & Flutter"
LEVEL = "Level"
RUMBLE = "Rumble"


def _create_label(x: int, y: int, text: str = "", color=WHITE) -> label.Label:
    return label.Label(terminalio.FONT, text=text, color=color, x=x, y=y)


class ButtonsHelper:
    """This class helps check the state of the buttons"""

    def __init__(self, button_tuple: tuple[bool, bool, bool]) -> None:
        self.buttons = button_tuple

    def is_a(self) -> bool:
        """Returns the state of the A button."""
        return self.buttons[0]

    def is_b(self) -> bool:
        """Returns the state of the B button."""
        return self.buttons[1]

    def is_c(self) -> bool:
        """Returns the state of the C button."""
        return self.buttons[2]


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
        self._width = int(os.getenv("CIRCUITPY_DISPLAY_WIDTH", "128"))
        self._height = int(os.getenv("CIRCUITPY_DISPLAY_HEIGHT", "64"))

        display_bus = I2CDisplayBus(i2c, device_address=DEVICE_ADDRESS)

        self.display = SH1107(display_bus, width=self._width, height=self._height)

        # Make the display context
        self._main_menu = MainScreen(self._width)

        self._rpm_screen = RPMScreen()
        self.leveling_screen = LevelingScreen()

        self.display.root_group = self._main_menu.get_group()

        # Debug Screen elements
        self.debug_group = displayio.Group()
        self.text_acceleration = _create_label(x=8, y=8)
        self.text_gyro = _create_label(x=8, y=18)
        self.text_rpm = _create_label(x=8, y=26)
        self.text_degree = _create_label(x=8, y=34)

        for debug_labels in [
            self.text_acceleration,
            self.text_gyro,
            self.text_rpm,
            self.text_degree,
        ]:
            self.debug_group.append(debug_labels)

    def width(self) -> int:
        """Return the width of the screen"""
        return self._width

    def height(self) -> int:
        """Returns the height of the screen"""
        return self._height

    def check_buttons(self) -> tuple[bool, bool, bool]:
        """checkes which button is pushed on the screen"""
        return (
            not self.button_a.value,
            not self.button_b.value,
            not self.button_c.value,
        )

    def draw_menu(self, mode: int) -> None:
        if mode == Mode.MAIN_MENU:
            self.display.root_group = self._main_menu.get_group()
        elif mode == Mode.RPM:
            self.display.root_group = self._rpm_screen.get_group()
        elif mode == Mode.LEVEL:
            self.display.root_group = self.leveling_screen.get_group()
        elif mode == Mode.RUMBLE:
            self.display.root_group = None
        else:
            self.display.root_group = self.debug_group

    def draw_rpm(self, rpm: float) -> None:
        self._rpm_screen.update(rpm)

    def draw_level(self, x: float, y: float) -> None:
        self.leveling_screen.update(x, y)

    def draw_rumble(self) -> None:
        pass

    def draw_debug(self, sensor: MemsSensor) -> None:
        """This will draw raw sensor values to the screen"""
        acc_x, acc_y, acc_z = sensor.get_acceleration()
        gyro_x, gyro_y, gyro_z = sensor.get_gyro()
        rpm = sensor.get_rpm()
        degree = sensor.get_degrees()

        self.text_acceleration.text = f"X{acc_x:.2f},Y{acc_y:.2f},Z{acc_z:.2f} m/s^2"
        self.text_gyro.text = f"X:{gyro_x:.2f},Y:{gyro_y:.2f},Z:{gyro_z:.2f} radians/s"
        self.text_rpm.text = f"RPM:{rpm:.2f}"
        self.text_degree.text = f"Degree:{degree:.2f}"
