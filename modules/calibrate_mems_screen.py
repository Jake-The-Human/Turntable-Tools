"""Draw the calibration results to the screen"""

import displayio
from adafruit_display_text import label

from .display import Display
from .calibrate_mems_mode import CalibrateMemsMode
from .helper import DisplayColor, STRINGS, FONT


class CalibrateMemsScreen:
    def __init__(self) -> None:
        self._calibrate_group = displayio.Group()
        self._text_progress = label.Label(
            FONT, text=STRINGS.START_TURNTABLE, color=DisplayColor.WHITE, scale=2, y=28
        )

        self._text_progress.hidden = True

        self._result_group = displayio.Group()
        text_accel_tag = label.Label(
            FONT, text=STRINGS.ACCEL_OFFSET, color=DisplayColor.WHITE, y=8
        )

        self._text_accelerometer_offset = label.Label(
            FONT, color=DisplayColor.WHITE, y=20
        )

        text_gyro_tag = label.Label(
            FONT, text=STRINGS.GYRO_OFFSET, color=DisplayColor.WHITE, y=38
        )

        self._text_gyro_offset = label.Label(FONT, color=DisplayColor.WHITE, y=50)

        self._result_group.append(text_accel_tag)
        self._result_group.append(self._text_accelerometer_offset)
        self._result_group.append(text_gyro_tag)
        self._result_group.append(self._text_gyro_offset)

        self._calibrate_group.append(self._text_progress)
        self._calibrate_group.append(self._result_group)

    def show_screen(self, screen: Display) -> None:
        """update display to calibration"""
        screen.set_display(self._calibrate_group)

    def update(self, calibrate_mode: CalibrateMemsMode) -> None:
        """Update the rumble number on screen"""
        if calibrate_mode.is_recording_data():
            self._text_progress.text = STRINGS.CALIBRATING

        elif calibrate_mode.is_starting_data():
            self._text_progress.hidden = False
            self._result_group.hidden = True
            self._text_progress.text = STRINGS.START_TURNTABLE

        elif not calibrate_mode.is_recording_data():
            self._text_progress.hidden = True
            self._result_group.hidden = False

            accel_x, accel_y, accel_z = calibrate_mode.acceleration_offset
            gyro_x, gyro_y, gyro_z = calibrate_mode.gyro_offset
            self._text_accelerometer_offset.text = (
                f"{accel_x:.2f} {accel_y:.2f} {accel_z:.2f}"
            )
            self._text_gyro_offset.text = f"{gyro_x:.2f} {gyro_y:.2f} {gyro_z:.2f}"
