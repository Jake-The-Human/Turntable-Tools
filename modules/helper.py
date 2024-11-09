"""Constants used through out the program"""

import terminalio

# SH1107 is vertically oriented 64x128
CIRCUITPY_DISPLAY_WIDTH: int = 128
CIRCUITPY_DISPLAY_HEIGHT: int = 64

# Display colors
WHITE: int = 0xFFFFFF
BLACK: int = 0x000000

# Font...
FONT = terminalio.FONT

# Common RPMs of turntables
RPM_33: float = 33.3333333333
RPM_45: float = 45.0
RPM_78: float = 78.0

# These are for when capturing rpm data
RPM_TEST_START_UP_TIME: float = 10
RPM_TEST_LEN: float = 30


class Mode:
    """These constants are used to describe what Mode the device is in"""

    DEBUG = -1
    MAIN_MENU = 0
    RPM = 1
    LEVEL = 2
    RUMBLE = 3


class STRINGS:
    """String used through out device"""

    TITLE = "Turntable Tool"
    RPM_WOW = "RPM & Wow"
    RPM = "RPM"
    LEVEL = "Level"
    RUMBLE = "Rumble"

    START_TURNTABLE = "Starting"
    MEASURING = "Measuring"

    AVG = "Avg"
    MIN = "Min"
    MAX = "Max"
    WOW = "Wow"
