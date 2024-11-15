"""Constants used through out the program"""

import time
import board
import terminalio
from displayio import Palette

# Pins and address
DISPLAY_ADDRESS = 0x3C
A_BUTTON_PIN = board.D9
B_BUTTON_PIN = board.D6
C_BUTTON_PIN = board.D5
BATTERY_VOLTAGE_PIN = board.A3

# SH1107 is vertically oriented 64x128
CIRCUITPY_DISPLAY_WIDTH: int = 128
CIRCUITPY_DISPLAY_HEIGHT: int = 64

# Battery info
REFERENCE_VOLTAGE: float = 3.3
BATTERY_MIN_VOLTAGE: float = 3.0
BATTERY_MAX_VOLTAGE: float = 4.2

# Turn extra features on/off
HAS_SD_CARD: bool = True
HAS_BATTERY_STATUS_CIRCUIT: bool = False
HAS_AZIMUTH_CIRCUIT: bool = False

# Font...
FONT = terminalio.FONT

# Common RPMs of turntables
RPM_33: float = 100.0 / 3.0
RPM_45: float = 45.0
RPM_78: float = 78.0

# Leveling debug
SHOW_X_Y = True

# These are for when capturing data
RPM_TEST_START_UP_TIME: float = 10
RPM_TEST_LEN: float = 30
RUMBLE_TEST_START_UP_TIME: float = 10
RUMBLE_TEST_LEN: float = 30

# Black and white color palettes
BLACK_PALETTE = Palette(1)
BLACK_PALETTE[0] = 0x000000

WHITE_PALETTE = Palette(1)
WHITE_PALETTE[0] = 0xFFFFFF


class UpdateGui:
    """The purpose of this class is to separate the data collection from the screen updating"""

    def __init__(self) -> None:
        self.gui_update_time: float = 0.033
        self.timer: float = time.time()
        self.callback: any

    def update(self) -> None:
        if (
            self.callback is not None
            and time.time() - self.timer >= self.gui_update_time
        ):
            self.callback()
            self.timer = time.time()


class DisplayColor:
    """Colors for the display"""

    WHITE: int = 0xFFFFFF
    BLACK: int = 0x000000


class PixelColor:
    """Colors for NeoPixel"""

    OFF: tuple = (0, 0, 0)
    GREEN: tuple = (0, 255, 0)
    YELLOW: tuple = (255, 255, 0)
    RED: tuple = (255, 0, 0)


class Mode:
    """These constants are used to describe what Mode the device is in"""

    DEBUG = -2
    MAIN_MENU = -1
    RPM = 0
    LEVEL = 1
    RUMBLE = 2
    AZIMUTH = 3
    ABOUT = 4


class STRINGS:
    """String used through out device"""

    TITLE = "Turntable Tool"
    RPM_WOW = "RPM & Wow"
    RPM = "RPM"
    LEVEL = "Level"
    RUMBLE = "Rumble"
    AZIMUTH = "Azimuth"
    ABOUT = "About"

    START_TURNTABLE = "Starting"
    MEASURING = "Measuring"

    AVG = "Avg"
    MIN = "Min"
    MAX = "Max"
    WOW = "Wow"
    FLUTTER = "Flutter"
    WOW_AND_FLUTTER = "W&F"

    NO_CIRCUIT = "circuit is\nnot present."
