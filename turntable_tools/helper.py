"""Constants and other data used through out the program"""

import board
import terminalio
from microcontroller import Pin

# Turn features on/off
HAS_MEMS_CIRCUIT: bool = True
HAS_ADC_CIRCUIT: bool = True
HAS_BATTERY_STATUS_CIRCUIT: bool = True
HAS_SD_CARD: bool = True

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

# Leveling debug
SHOW_X_Y: bool = False

# These are for when capturing data
RPM_TEST_START_UP_TIME: float = 10
RPM_TEST_LEN: float = 30
RUMBLE_TEST_START_UP_TIME: float = 10
RUMBLE_TEST_LEN: float = 30
CALIBRATION_TEST_START_UP_TIME: float = 5
CALIBRATION_TEST_LEN: float = 5

TEST_RECORDS: dict = {
    "Ortofon Test Record": ["left", "right", "left", "right"],
    "Analogue Productions Ultimate Analogue Test Record": ["left", "right"],
}
