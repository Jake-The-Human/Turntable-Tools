import board
import digitalio
from adafruit_debouncer import Button

_A_BUTTON_INDEX = 0
_B_BUTTON_INDEX = 1
_C_BUTTON_INDEX = 2


class Buttons:
    def __init__(self) -> None:
        pin_c = digitalio.DigitalInOut(board.D5)
        pin_c.switch_to_input(pull=digitalio.Pull.UP)

        pin_b = digitalio.DigitalInOut(board.D6)
        pin_b.switch_to_input(pull=digitalio.Pull.UP)

        pin_a = digitalio.DigitalInOut(board.D9)
        pin_a.switch_to_input(pull=digitalio.Pull.UP)

        self._buttons = [Button(pin_a), Button(pin_b), Button(pin_c)]

    def update(self) -> None:
        for button in self._buttons:
            button.update()

    def a_pressed(self) -> bool:
        return self._buttons[_A_BUTTON_INDEX].pressed

    def b_pressed(self) -> bool:
        return self._buttons[_B_BUTTON_INDEX].pressed

    def c_pressed(self) -> bool:
        return self._buttons[_C_BUTTON_INDEX].pressed
