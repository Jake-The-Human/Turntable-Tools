"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: helper.py
Description: Constants and other data used through out the program.

Author: Jake-The-Human
Repository: https://github.com/Jake-The-Human/Turntable-Tools
License: GPL-3.0-or-later (see LICENSE file for details)
Date Created: 2024-12-17

This file is part of Turntable Tools.

Turntable Tools is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Turntable Tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Turntable Tools. If not, see <https://www.gnu.org/licenses/>.
"""

import board
import terminalio
from microcontroller import Pin

# Turn features on/off
HAS_MEMS_CIRCUIT: bool = True
HAS_ADC_CIRCUIT: bool = False
HAS_BATTERY_STATUS_CIRCUIT: bool = True
HAS_SD_CARD: bool = True
# Leveling debug
SHOW_X_Y: bool = False

# Pins and address
DISPLAY_ADDRESS = 0x3C

A_BUTTON_PIN: Pin = board.D9
B_BUTTON_PIN: Pin = board.D6
C_BUTTON_PIN: Pin = board.D5

LEFT_CH_PIN = board.A0
RIGHT_CH_PIN = board.A1

BATTERY_VOLTAGE_PIN: Pin = board.A3

# SH1107 is vertically oriented 64x128
CIRCUITPY_DISPLAY_WIDTH: int = 128
CIRCUITPY_DISPLAY_HEIGHT: int = 64

# Battery info
REFERENCE_VOLTAGE: float = 3.3
BATTERY_MIN_VOLTAGE: float = 3.0
BATTERY_MAX_VOLTAGE: float = 4.2
MAX_INT_16: int = 65535

# Font...
FONT = terminalio.FONT

# Common RPMs of turntables
RPM_33: float = 100.0 / 3.0
RPM_45: float = 45.0
RPM_78: float = 78.0

# These are for when capturing data
RPM_TEST_START_UP_TIME: float = 10.0
RPM_TEST_LEN: float = 30.0
RUMBLE_TEST_START_UP_TIME: float = 10.0
RUMBLE_TEST_LEN: float = 30.0
CALIBRATION_TEST_START_UP_TIME: float = 5.0
CALIBRATION_TEST_LEN: float = 5.0

TEST_RECORDS: dict = {
    "Ortofon Test Record": ["left", "right", "left", "right"],
    "Analogue Productions Ultimate Analogue Test Record": ["left", "right"],
}
