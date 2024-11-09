import time
import displayio
from adafruit_display_text import label

from .display import Display
from .helper import WHITE, FONT, STRINGS


class RPMScreen:
    def __init__(self) -> None:
        self.rpm_group = displayio.Group()
        self._text_rpm = label.Label(FONT, color=WHITE, scale=3, x=0, y=16)
        text_rpm_unit = label.Label(
            FONT, text=STRINGS.RPM, color=WHITE, scale=2, x=88, y=16
        )
        self._text_progress = label.Label(FONT, color=WHITE, scale=2, x=0, y=42)
        self._text_avg = label.Label(FONT, color=WHITE, x=0, y=36)
        self._text_min_max = label.Label(FONT, color=WHITE, x=0, y=45)
        self._text_wow = label.Label(FONT, color=WHITE, x=0, y=54)
        self.rpm_group.append(self._text_rpm)
        self.rpm_group.append(text_rpm_unit)
        self.rpm_group.append(self._text_progress)
        self.rpm_group.append(self._text_avg)
        self.rpm_group.append(self._text_min_max)
        self.rpm_group.append(self._text_wow)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the RPM tool"""
        screen.set_display(self.rpm_group)

    def update(self, rpm: float) -> None:
        """Update the RPM number on screen"""
        self._text_rpm.text = f"{rpm:.2f}"

    def start_recording_data(self, start_up_time: float) -> None:
        """This function is called when you want to start recording RPM"""
        self._text_rpm.text = f"{0:.2f}"
        self._text_progress.text = STRINGS.START_TURNTABLE
        time.sleep(start_up_time)  # sleep for 5 sec to let turntable get up to speed
        self._text_progress.text = STRINGS.MEASURING

    def stop_recording_data(
        self, rpm_results: tuple[float, float, float, float]
    ) -> None:
        """Prints the results to the screen from the record data"""
        avg_rpm, min_rpm, max_rpm, wow = rpm_results
        self._text_progress.hidden = True
        self._text_avg.text = f"{STRINGS.AVG}: {avg_rpm:.2f}"
        self._text_min_max.text = (
            f"{STRINGS.MIN}: {min_rpm:.2f} {STRINGS.MAX}: {max_rpm:.2f}"
        )
        self._text_wow.text = f"{STRINGS.WOW}: {wow:.2f}%"
