class RPMMode:
    def __init__(self) -> None:
        self._buffer_index: int = 0
        self._buffer: list[float] = [0, 0, 0]
        self._rpm_data: list = []
        self._record_data: bool = False

    def _get_buffer_index(self) -> int:
        self._buffer_index = (self._buffer_index + 1) % len(self._buffer)
        return self._buffer_index

    def update(self, rpm: float) -> float:
        """This returns normilized rpm data"""
        self._buffer[self._get_buffer_index()] = rpm
        new_rpm: float = sum(self._buffer) / len(self._buffer)
        if self._record_data:
            self._rpm_data.append(new_rpm)
        return new_rpm

    def start(self):
        """Start recording data for the wow and flutter calc"""
        self._record_data = True

    def stop(self):
        """Stop recording data for the wow and flutter calc"""
        self._record_data = False
        # do something with wow and flutter

    def wow(self, nominal_rpm):
        # Calculate the difference between each measured RPM and the nominal RPM
        deviations = [abs(rpm - nominal_rpm) for rpm in self._rpm_data]

        # Calculate the wow as the maximum deviation (slow speed variations)
        wow = max(deviations) / nominal_rpm * 100
        return wow, deviations

    def flutter(self, nominal_rpm):
        # Calculate short-term deviations between consecutive RPM values
        flutter_deviations = [
            abs(self._rpm_data[i] - self._rpm_data[i - 1])
            for i in range(1, len(self._rpm_data))
        ]

        # Calculate flutter as the maximum short-term deviation, in percentage terms
        flutter = max(flutter_deviations) / nominal_rpm * 100  # Convert to percentage
        return flutter, flutter_deviations
