"""Constants used through out the program"""
import terminalio

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

    DEBUG: int = -1
    MAIN_MENU: int = 0
    RPM: int = 1
    LEVEL: int = 2
    RUMBLE: int = 3

class STRINGS:
    """String used through out device"""
    TITLE: str = "Turntable Tool"
    RPM_WOW: str = "RPM & Wow"
    RPM: str = "RPM"
    LEVEL: str = "Level"
    RUMBLE: str = "Rumble"

    START_TURNTABLE: str = "Starting"
    MEASURING: str = "Measuring"

    AVG: str = "Avg"
    MIN: str = "Min"
    MAX: str = "Max"
    WOW: str = "Wow"
