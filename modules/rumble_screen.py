from math import log
import displayio
from adafruit_display_text import label

from .display import Display
from .rumble_mode import RumbleMode
from .helper import FONT, DisplayColor, STRINGS


INTENSITY_INDEX = 0
AVG_X_INDEX = 1
AVG_Y_INDEX = 2
AVG_Z_INDEX = 3


class RumbleScreen:
    def __init__(self) -> None:
        self._rumble_group = displayio.Group()
        self._text_progress = label.Label(
            FONT, color=DisplayColor.WHITE, scale=2, x=0, y=28
        )

        self._result_group = displayio.Group()
        self._rumble_data = []
        for i in range(4):
            self._rumble_data.append(
                label.Label(FONT, text=" ", color=DisplayColor.WHITE, padding_left=1)
            )
            self._rumble_data[i].x = 1
            self._rumble_data[i].y = 8 + (self._rumble_data[i].height * i)
            self._result_group.append(self._rumble_data[i])

        self._rumble_group.append(self._text_progress)
        self._rumble_group.append(self._result_group)

    def show_screen(self, screen: Display) -> None:
        """This will make the display rumble screen"""
        screen.set_display(self._rumble_group)

    def update(self, rumble_mode: RumbleMode) -> None:
        if rumble_mode.is_recording_data():
            self._text_progress.text = STRINGS.MEASURING

        elif rumble_mode.is_starting_data():
            self._text_progress.hidden = False
            self._result_group.hidden = True
            self._text_progress.text = STRINGS.START_TURNTABLE

        elif not rumble_mode.is_recording_data():
            self._text_progress.hidden = True
            self._result_group.hidden = False
            avg_x, avg_y, avg_z, rumble_intensity = rumble_mode.get_results()
            self._rumble_data[INTENSITY_INDEX].text = (
                f"Intensity: {self._acceleration_to_db(rumble_intensity):.2f}dB"
            )
            self._rumble_data[AVG_X_INDEX].text = (
                f"Avg X: {self._acceleration_to_db(avg_x):.2f}dB"
            )
            self._rumble_data[AVG_Y_INDEX].text = (
                f"Avg Y: {self._acceleration_to_db(avg_y):.2f}dB"
            )
            self._rumble_data[AVG_Z_INDEX].text = (
                f"Avg Z: {self._acceleration_to_db(avg_z):.2f}db"
            )

    def _acceleration_to_db(self, accel_value: float, a_ref: float = 9.81) -> float:
        """Convert acceleration to decibels (relative to a_ref)."""
        return (
            20.0 * log(abs(accel_value) / a_ref, 10)
            if accel_value != 0
            else -float("inf")
        )
