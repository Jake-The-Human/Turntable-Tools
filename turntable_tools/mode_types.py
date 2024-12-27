"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: mode_types.py
Description: These constants are used to describe what Mode the device is in.

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

from turntable_tools import strings as STRINGS

DEBUG: int = -2
MAIN_MENU: int = -1
RPM: int = 0
LEVEL: int = 1
RUMBLE: int = 2
AZIMUTH: int = 3
CALIBRATE_MEMS: int = 6
ABOUT: int = 7

MODE_TO_STR: dict = {
    DEBUG: STRINGS.DEBUG,
    MAIN_MENU: STRINGS.MAIN_MENU,
    RPM: STRINGS.RPM,
    LEVEL: STRINGS.LEVEL,
    RUMBLE: STRINGS.RUMBLE,
    AZIMUTH: STRINGS.AZIMUTH,
    CALIBRATE_MEMS: STRINGS.CALIBRATE_MEMS,
    ABOUT: STRINGS.ABOUT,
}
