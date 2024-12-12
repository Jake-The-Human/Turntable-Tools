import time
from neopixel import NeoPixel
from .mems_sensor import MemsSensor
from .buttons import Buttons
from . import colors as COLORS
from .helper import (
    RPM_33,
    RPM_45,
    RPM_78,
    RPM_TEST_START_UP_TIME,
    RPM_TEST_LEN,
    HAS_SD_CARD,
)

_TOTAL_TEST_LEN = RPM_TEST_LEN + RPM_TEST_START_UP_TIME


def _wow(rpm_data: list[float], nominal_rpm: float) -> float:
    """This calculates the wow supposedly..."""
    # Calculate the difference between each measured RPM and the nominal RPM
    deviations: float = [abs(rpm - nominal_rpm) for rpm in rpm_data]

    # Calculate the wow as the maximum deviation (slow speed variations)
    return max(deviations) / nominal_rpm * 100.0


def _flutter(rpm_data: list[float], nominal_rpm: float) -> float:
    """NOTE flutter but not convinced i need this"""
    # Calculate short-term deviations between consecutive RPM values
    flutter_deviations: float = [
        abs(rpm_data[i] - rpm_data[i - 1]) for i in range(1, len(rpm_data))
    ]

    # Calculate flutter as the maximum short-term deviation, in percentage terms
    return max(flutter_deviations) / nominal_rpm * 100.0


class RPMMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel: NeoPixel = pixel
        self._rpm_data: list[float] = []
        self._time: float = 0

        self._record_data: bool = False
        self._start_up: bool = False
        self.current_rpm: float = 0
        self.result: tuple = (0, 0, 0, 0, 0)

    def handle_buttons(self, buttons: Buttons) -> None:
        """Any mode specific action that are triggered by a button"""
        if buttons.b_pressed():
            self.start()

    def update(self, sensor: MemsSensor) -> None:
        """This returns normalized rpm data"""
        new_rpm: float = sensor.get_rpm

        current_time = time.time() - self._time
        if RPM_TEST_START_UP_TIME <= current_time <= _TOTAL_TEST_LEN:
            self._pixel.fill(COLORS.NEO_PIXEL_GREEN)
            self._record_data = True
            self._start_up = False
            self._rpm_data.append(new_rpm)
        elif self._record_data:
            self.stop()
            # remove any noise or low rpms from the list
            # self._rpm_data = [d for d in self._rpm_data if d > 29]

            if self._rpm_data:
                rpm_avg: float = sum(self._rpm_data) / len(self._rpm_data)
                nominal_rpm: float = min(
                    [RPM_33, RPM_45, RPM_78], key=lambda x: abs(x - rpm_avg)
                )

                self.result = (
                    rpm_avg,
                    min(self._rpm_data),
                    max(self._rpm_data),
                    _wow(self._rpm_data, nominal_rpm),
                    _flutter(self._rpm_data, nominal_rpm),
                )
                self._rpm_data.clear()
                if HAS_SD_CARD:
                    self.write_results_to_file()

        self.current_rpm = new_rpm

    @property
    def is_recording_data(self) -> bool:
        """Is used to check if we are capturing rpm data"""
        return self._record_data

    @property
    def is_starting_data(self) -> bool:
        """Is used to check if we are letting the turntable get upto speed"""
        return self._start_up

    def start(self) -> None:
        """Start recording data for the wow and flutter calc"""
        self._pixel.fill(COLORS.NEO_PIXEL_YELLOW)
        self._start_up = True
        self._time = time.time()

    def stop(self) -> None:
        """Stop recording data for the wow and flutter calc"""
        self._pixel.fill(COLORS.NEO_PIXEL_RED)
        self._record_data = False
        self._time = 0

    def write_results_to_file(self) -> None:
        with open("/sd/rpm.txt", mode="a", encoding="ascii") as rpm_result:
            avg_rpm, min_rpm, max_rpm, wow, flutter = self.result
            rpm_result.write(
                f"Avg:{avg_rpm}, Min:{min_rpm}, Max:{max_rpm}, Wow:{wow}%, Flutter:{flutter}%\n"
            )
