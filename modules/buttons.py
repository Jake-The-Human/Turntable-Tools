import digitalio
from adafruit_debouncer import Button
from .helper import A_BUTTON_PIN, B_BUTTON_PIN, C_BUTTON_PIN

_A_BUTTON_INDEX = 0
_B_BUTTON_INDEX = 1
_C_BUTTON_INDEX = 2


class Buttons:
    def __init__(self) -> None:
        pin_c = digitalio.DigitalInOut(C_BUTTON_PIN)
        pin_c.switch_to_input(pull=digitalio.Pull.UP)

        pin_b = digitalio.DigitalInOut(B_BUTTON_PIN)
        pin_b.switch_to_input(pull=digitalio.Pull.UP)

        pin_a = digitalio.DigitalInOut(A_BUTTON_PIN)
        pin_a.switch_to_input(pull=digitalio.Pull.UP)

        self._buttons = [Button(pin_a), Button(pin_b), Button(pin_c)]

    def update(self) -> None:
        """Updates the state of the buttons to see if any new events have happened"""
        for button in self._buttons:
            button.update()

    def a_pressed(self) -> bool:
        """See if the A button has been pressed"""
        return self._buttons[_A_BUTTON_INDEX].pressed

    def b_pressed(self) -> bool:
        """See if the B button has been pressed"""
        return self._buttons[_B_BUTTON_INDEX].pressed

    def c_pressed(self) -> bool:
        """See if the C button has been pressed"""
        return self._buttons[_C_BUTTON_INDEX].pressed
