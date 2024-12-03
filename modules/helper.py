"""Constants and other data used through out the program"""

from time import time
import board
import terminalio
from microcontroller import Pin
from displayio import Palette

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
BATTERY_VOLTAGE_PIN: Pin = board.A3

# SH1107 is vertically oriented 64x128
CIRCUITPY_DISPLAY_WIDTH: int = 128
CIRCUITPY_DISPLAY_HEIGHT: int = 64

# Battery info
REFERENCE_VOLTAGE: float = 3.3
BATTERY_MIN_VOLTAGE: float = 3.0
BATTERY_MAX_VOLTAGE: float = 4.2

# Font...
FONT = terminalio.FONT

# Common RPMs of turntables
RPM_33: float = 100.0 / 3.0
RPM_45: float = 45.0
RPM_78: float = 78.0

# Leveling debug
SHOW_X_Y: bool = True

# These are for when capturing data
RPM_TEST_START_UP_TIME: float = 10
RPM_TEST_LEN: float = 30
RUMBLE_TEST_START_UP_TIME: float = 10
RUMBLE_TEST_LEN: float = 30
CALIBRATION_TEST_START_UP_TIME: float = 5
CALIBRATION_TEST_LEN: float = 5

# Black and white color palettes
BLACK_PALETTE = Palette(1)
BLACK_PALETTE[0] = 0x000000
WHITE_PALETTE = Palette(1)
WHITE_PALETTE[0] = 0xFFFFFF


class UpdateGui:
    """The purpose of this class is to separate the data collection from the screen updating"""

    def __init__(self) -> None:
        self.gui_update_time: float = 0.03
        self.timer: float = time()
        self.callback = UpdateGui._stub

    def update(self) -> None:
        """Check if enough time has pass before updating the gui"""
        # if time() - self.timer >= self.gui_update_time:
        self.callback()
        # self.timer = time()

    @staticmethod
    def _stub() -> None:
        pass


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


class STRINGS:
    """String used through out device"""

    TITLE = "Turntable Tool"
    RPM = "RPM"
    LEVEL = "Level"
    RUMBLE = "Rumble"
    AZIMUTH = "Azimuth"
    PHASE = "Phase"
    CALIBRATE_MEMS = "Calibrate MEMS"
    ABOUT = "About"

    START_TURNTABLE = "Starting"
    MEASURING = "Measuring"
    CALIBRATING = "Calibrating"

    AVG = "Avg"
    MIN = "Min"
    MAX = "Max"
    WOW_AND_FLUTTER = "W&F"
    INTENSITY = "Intensity"

    ACCEL_OFFSET = "Accel Offset"
    GYRO_OFFSET = "Gyro Offset"
    NO_CIRCUIT = "Circuit is not\npresent."


class Mode:
    """These constants are used to describe what Mode the device is in"""

    DEBUG = -2
    MAIN_MENU = -1
    RPM = 0
    LEVEL = 1
    RUMBLE = 2
    AZIMUTH = 3
    PHASE = 4
    CALIBRATE_MEMS = 6
    ABOUT = 7

    MODE_TO_STR = {
        DEBUG: "Debug",
        MAIN_MENU: "Main Menu",
        RPM: STRINGS.RPM,
        LEVEL: STRINGS.LEVEL,
        RUMBLE: STRINGS.RUMBLE,
        AZIMUTH: STRINGS.AZIMUTH,
        PHASE: STRINGS.PHASE,
        CALIBRATE_MEMS: STRINGS.CALIBRATE_MEMS,
        ABOUT: STRINGS.ABOUT,
    }
