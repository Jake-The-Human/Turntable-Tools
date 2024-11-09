from .helper import RPM_33, RPM_45, RPM_78


class RPMMode:
    def __init__(self) -> None:
        self._buffer_index: int = 0
        self._buffer_len: int = 5
        self._buffer: list[float] = [0 for _ in range(self._buffer_len)]
        self._rpm_data: list[float] = []
        self._record_data: bool = False

    def _get_buffer_index(self) -> int:
        self._buffer_index = (self._buffer_index + 1) % self._buffer_len
        return self._buffer_index

    def update(self, rpm: float) -> float:
        """This returns normilized rpm data"""
        self._buffer[self._get_buffer_index()] = rpm
        new_rpm: float = sum(self._buffer) / self._buffer_len
        if self._record_data:
            self._rpm_data.append(new_rpm)
        return new_rpm

    def is_recording_data(self) -> bool:
        return self._record_data

    def start(self) -> None:
        """Start recording data for the wow and flutter calc"""
        self._record_data = True

    def stop(self) -> tuple[float, float, float, float]:
        """Stop recording data for the wow and flutter calc"""
        self._record_data = False
        # do something with wow and flutter
        self._rpm_data = [d for d in self._rpm_data if d > 29]
        # print(self.flutter(RPM_33))
        if self._rpm_data == []:
            return 0, 0, 0, 0
        return (sum(self._rpm_data) / len(self._rpm_data)), min(self._rpm_data), max(self._rpm_data), self.wow(RPM_33)

    def wow(self, nominal_rpm: float) -> float:
        # Calculate the difference between each measured RPM and the nominal RPM
        deviations = [abs(rpm - nominal_rpm) for rpm in self._rpm_data]

        # Calculate the wow as the maximum deviation (slow speed variations)
        wow = max(deviations) / nominal_rpm * 100
        return wow

    def flutter(self, nominal_rpm: float) -> float:
        # Calculate short-term deviations between consecutive RPM values
        flutter_deviations = [
            abs(self._rpm_data[i] - self._rpm_data[i - 1])
            for i in range(1, len(self._rpm_data))
        ]

        # Calculate flutter as the maximum short-term deviation, in percentage terms
        flutter = max(flutter_deviations) / nominal_rpm * 100  # Convert to percentage
        return flutter
