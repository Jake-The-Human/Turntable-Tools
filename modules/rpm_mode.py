import time
from neopixel import NeoPixel
from .helper import (
    RPM_33,
    RPM_45,
    RPM_78,
    RPM_TEST_START_UP_TIME,
    RPM_TEST_LEN,
    HAS_SD_CARD,
    PixelColor,
)

MOVING_AVG_SIZE: int = 10
TOTAL_TEST_LEN = RPM_TEST_LEN + RPM_TEST_START_UP_TIME


class RPMMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self._buffer_index: int = 0
        self._buffer_len: int = MOVING_AVG_SIZE
        self._buffer: list[float] = [0 for _ in range(self._buffer_len)]
        self._rpm_data: list[float] = []
        self._record_data: bool = False
        self._start_up: bool = False
        self._time: float = 0
        self._result: tuple = (0, 0, 0, 0, 0)

    def _get_buffer_index(self) -> int:
        """This is for the moving average index so it does not go out of bounds"""
        self._buffer_index = (self._buffer_index + 1) % self._buffer_len
        return self._buffer_index

    def get_results(self) -> tuple[float, float, float, float, float]:
        return self._result

    def update(self, rpm: float) -> float:
        """This returns normalized rpm data"""
        self._buffer[self._get_buffer_index()] = rpm
        new_rpm: float = sum(self._buffer) / self._buffer_len

        current_time = time.time() - self._time
        if current_time > RPM_TEST_START_UP_TIME and current_time <= TOTAL_TEST_LEN:
            self._pixel.fill(PixelColor.GREEN)
            self._record_data = True
            self._start_up = False
            self._rpm_data.append(new_rpm)
        elif self._record_data:
            self.stop()
            # remove any noise or low rpms from the list
            self._rpm_data = [d for d in self._rpm_data if d > 29]

            if self._rpm_data != []:
                rpm_avg: float = sum(self._rpm_data) / len(self._rpm_data)
                nominal_rpm: float = min(
                    [RPM_33, RPM_45, RPM_78], key=lambda x: abs(x - rpm_avg)
                )

                self._result = (
                    rpm_avg,
                    min(self._rpm_data),
                    max(self._rpm_data),
                    self.wow(nominal_rpm),
                    self.flutter(nominal_rpm),
                )
                self._rpm_data.clear()
                if HAS_SD_CARD:
                    with open("/sd/rpm.txt", mode="a", encoding="ascii") as rpm_result:
                        avg_rpm, min_rpm, max_rpm, wow, flutter = self._result
                        rpm_result.write(
                            f"Avg:{avg_rpm}, Min:{min_rpm}, Max:{max_rpm}, Wow:{wow}%, Flutter:{flutter}%\n"
                        )

        return new_rpm

    def is_recording_data(self) -> bool:
        """Is used to check if we are capturing rpm data"""
        return self._record_data

    def is_starting_data(self) -> bool:
        """Is used to check if we are letting the turntable get upto speed"""
        return self._start_up

    def start(self) -> None:
        """Start recording data for the wow and flutter calc"""
        self._pixel.fill(PixelColor.YELLOW)
        self._start_up = True
        self._time = time.time()

    def stop(self) -> None:
        """Stop recording data for the wow and flutter calc"""
        self._pixel.fill(PixelColor.RED)
        self._record_data = False
        self._time = 0

    def wow(self, nominal_rpm: float) -> float:
        """This calculates the wow supposedly..."""
        # Calculate the difference between each measured RPM and the nominal RPM
        deviations = [abs(rpm - nominal_rpm) for rpm in self._rpm_data]

        # Calculate the wow as the maximum deviation (slow speed variations)
        wow = max(deviations) / nominal_rpm * 100
        return wow

    def flutter(self, nominal_rpm: float) -> float:
        """NOTE flutter but not convinced i need this"""
        # Calculate short-term deviations between consecutive RPM values
        flutter_deviations = [
            abs(self._rpm_data[i] - self._rpm_data[i - 1])
            for i in range(1, len(self._rpm_data))
        ]

        # Calculate flutter as the maximum short-term deviation, in percentage terms
        flutter = max(flutter_deviations) / nominal_rpm * 100  # Convert to percentage
        return flutter
