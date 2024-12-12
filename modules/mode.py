"""These constants are used to describe what Mode the device is in"""

from . import strings as STRINGS

DEBUG: int = -2
MAIN_MENU: int = -1
RPM: int = 0
LEVEL: int = 1
RUMBLE: int = 2
AZIMUTH: int = 3
CALIBRATE_MEMS: int = 6
ABOUT: int = 7

MODE_TO_STR: dict = {
    DEBUG: "Debug",
    MAIN_MENU: "Main Menu",
    RPM: STRINGS.RPM,
    LEVEL: STRINGS.LEVEL,
    RUMBLE: STRINGS.RUMBLE,
    AZIMUTH: STRINGS.AZIMUTH,
    CALIBRATE_MEMS: STRINGS.CALIBRATE_MEMS,
    ABOUT: STRINGS.ABOUT,
}
