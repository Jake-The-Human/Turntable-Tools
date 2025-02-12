"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: buttons.py
Description: Handles Button presses.

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

from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Button

from turntable_tools.helper import A_BUTTON_PIN, B_BUTTON_PIN, C_BUTTON_PIN

_A_BUTTON_INDEX: int = 0
_B_BUTTON_INDEX: int = 1
_C_BUTTON_INDEX: int = 2

_TIMEOUT: float = 5.0


class Buttons:
    """This class wraps the 3 button logic"""

    def __init__(self) -> None:
        pin_c = DigitalInOut(C_BUTTON_PIN)
        pin_c.switch_to_input(pull=Pull.UP)

        pin_b = DigitalInOut(B_BUTTON_PIN)
        pin_b.switch_to_input(pull=Pull.UP)

        pin_a = DigitalInOut(A_BUTTON_PIN)
        pin_a.switch_to_input(pull=Pull.UP)

        self._buttons = [Button(pin_a), Button(pin_b), Button(pin_c)]

    def update(self) -> None:
        """Updates the state of the buttons to see if any new events have happened"""
        for button in self._buttons:
            button.update()

    def inactive(self) -> bool:
        """TODO Work in progress..."""
        result = False
        for b in self._buttons:
            result = (not b.current_duration <= _TIMEOUT) or result
            print(b.current_duration)
        return result

    @property
    def a_pressed(self) -> bool:
        """See if the A button has been pressed"""
        return self._buttons[_A_BUTTON_INDEX].pressed

    @property
    def b_pressed(self) -> bool:
        """See if the B button has been pressed"""
        return self._buttons[_B_BUTTON_INDEX].pressed

    @property
    def c_pressed(self) -> bool:
        """See if the C button has been pressed"""
        return self._buttons[_C_BUTTON_INDEX].pressed
