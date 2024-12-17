"""Draw the calibration results to the screen"""

import displayio
from adafruit_display_text import label

from turntable_tools.modes.calibrate_mems_mode import CalibrateMemsMode
from turntable_tools import colors as COLORS
from turntable_tools import strings as STRINGS
from turntable_tools.helper import FONT


class CalibrateMemsScreen(displayio.Group):
    """This is the screen for calibrating the mems sensor"""

    def __init__(self) -> None:
        super().__init__()
        self._text_progress = label.Label(
            FONT,
            text=STRINGS.START_TURNTABLE,
            color=COLORS.DISPLAY_WHITE,
            scale=2,
            y=28,
        )

        self._text_progress.hidden = True

        self._result_group = displayio.Group()
        text_accel_tag = label.Label(
            FONT, text=STRINGS.ACCEL_OFFSET, color=COLORS.DISPLAY_WHITE, y=8
        )

        self._text_accelerometer_offset = label.Label(
            FONT, color=COLORS.DISPLAY_WHITE, y=20
        )

        text_gyro_tag = label.Label(
            FONT, text=STRINGS.GYRO_OFFSET, color=COLORS.DISPLAY_WHITE, y=38
        )

        self._text_gyro_offset = label.Label(FONT, color=COLORS.DISPLAY_WHITE, y=50)

        self._result_group.append(text_accel_tag)
        self._result_group.append(self._text_accelerometer_offset)
        self._result_group.append(text_gyro_tag)
        self._result_group.append(self._text_gyro_offset)

        self.append(self._text_progress)
        self.append(self._result_group)

    def update(self, calibrate_mode: CalibrateMemsMode) -> None:
        """Update the rumble number on screen"""
        if calibrate_mode.is_recording_data:
            self._text_progress.text = STRINGS.CALIBRATING

        elif calibrate_mode.is_starting_data:
            self._text_progress.hidden = False
            self._result_group.hidden = True
            self._text_progress.text = STRINGS.START_TURNTABLE

        elif not calibrate_mode.is_recording_data:
            self._text_progress.hidden = True
            self._result_group.hidden = False

            accel_x, accel_y, accel_z = calibrate_mode.acceleration_offset
            gyro_x, gyro_y, gyro_z = calibrate_mode.gyro_offset
            self._text_accelerometer_offset.text = (
                f"{accel_x:.2f} {accel_y:.2f} {accel_z:.2f}"
            )
            self._text_gyro_offset.text = f"{gyro_x:.2f} {gyro_y:.2f} {gyro_z:.2f}"
