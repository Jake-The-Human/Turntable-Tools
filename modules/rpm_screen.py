import displayio
from adafruit_display_text import label

from .display import Display
from .rpm_mode import RPMMode
from .helper import DisplayColor, STRINGS, FONT


class RPMScreen:
    def __init__(self) -> None:
        self._rpm_group = displayio.Group()
        self._text_rpm = label.Label(FONT, color=DisplayColor.WHITE, scale=3, y=16)
        text_rpm_unit = label.Label(
            FONT, text=STRINGS.RPM, color=DisplayColor.WHITE, scale=2, x=88, y=16
        )
        self._text_progress = label.Label(FONT, color=DisplayColor.WHITE, scale=2, y=42)

        self._result_group = displayio.Group()
        self._text_avg = label.Label(FONT, color=DisplayColor.WHITE, y=36)
        self._text_min_max = label.Label(FONT, color=DisplayColor.WHITE, y=46)
        self._text_wow = label.Label(FONT, color=DisplayColor.WHITE, y=56)

        self._result_group.append(self._text_avg)
        self._result_group.append(self._text_min_max)
        self._result_group.append(self._text_wow)

        self._rpm_group.append(self._text_rpm)
        self._rpm_group.append(text_rpm_unit)
        self._rpm_group.append(self._text_progress)
        self._rpm_group.append(self._result_group)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the RPM tool"""
        screen.set_display(self._rpm_group)

    def update(self, rpm_mode: RPMMode) -> None:
        """Update the RPM number on screen"""
        if rpm_mode.is_recording_data():
            self._text_progress.text = STRINGS.MEASURING

        elif rpm_mode.is_starting_data():
            self._text_progress.hidden = False
            self._result_group.hidden = True
            self._text_progress.text = STRINGS.START_TURNTABLE

        elif not rpm_mode.is_recording_data():
            avg_rpm, min_rpm, max_rpm, wow, flutter = rpm_mode.result
            self._text_progress.hidden = True
            self._result_group.hidden = False

            self._text_avg.text = f"{STRINGS.AVG}: {avg_rpm:.2f}"
            self._text_min_max.text = (
                f"{STRINGS.MIN}: {min_rpm:.2f} {STRINGS.MAX}: {max_rpm:.2f}"
            )
            self._text_wow.text = (
                f"{STRINGS.WOW_AND_FLUTTER}: {wow:.2f}% {flutter:.2f}%"
            )

        self._text_rpm.text = f"{rpm_mode.current_rpm:.2f}"
