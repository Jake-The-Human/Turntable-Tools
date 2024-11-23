from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Button
from .helper import A_BUTTON_PIN, B_BUTTON_PIN, C_BUTTON_PIN

_A_BUTTON_INDEX = 0
_B_BUTTON_INDEX = 1
_C_BUTTON_INDEX = 2

_TIMEOUT = 5.0


class Buttons:
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
        result = False
        for b in self._buttons:
            result = (not b.current_duration <= _TIMEOUT) or result
            print(b.current_duration)
        return result 

    def a_pressed(self) -> bool:
        """See if the A button has been pressed"""
        return self._buttons[_A_BUTTON_INDEX].pressed

    def b_pressed(self) -> bool:
        """See if the B button has been pressed"""
        return self._buttons[_B_BUTTON_INDEX].pressed

    def c_pressed(self) -> bool:
        """See if the C button has been pressed"""
        return self._buttons[_C_BUTTON_INDEX].pressed
