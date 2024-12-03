from math import sqrt
import board
from analogio import AnalogIn


SAMPLE_RATE = 10000 
_SAMPLE_BUFFER_SIZE: int = 128


def _value_to_voltage(value: int, voltage_ref: float) -> float:
    """Change raw value to voltage and subtract the DC offset"""
    return ((value / 65535) * voltage_ref) - (voltage_ref / 2.0)

class AdcSensor:
    def __init__(self) -> None:
        self.chan_one = AnalogIn(board.A0)
        self.chan_two = AnalogIn(board.A1)

        # RMS
        self._channel_index: int = 0
        self._channel_one_samples: list = [0.0] * _SAMPLE_BUFFER_SIZE
        self._channel_two_samples: list = [0.0] * _SAMPLE_BUFFER_SIZE
        self._sum_of_squares_1: float = 0.0
        self._sum_of_squares_2: float = 0.0
        self._samples_collected: int = 0  # Track the number of valid samples

    def update(self) -> None:
        """Update the buffer with new samples and maintain a running RMS."""
        new_sample_1 = _value_to_voltage(self.chan_one.value, self.chan_one.reference_voltage)
        new_sample_2 = _value_to_voltage(self.chan_two.value, self.chan_two.reference_voltage)
        # print(new_sample_1, new_sample_2, self.chan_one.reference_voltage)

        # Get the index of the sample to be replaced
        oldest_sample_index = self._channel_index
        old_sample_1 = self._channel_one_samples[oldest_sample_index]
        old_sample_2 = self._channel_two_samples[oldest_sample_index]

        # Update the sum of squares by removing the old sample contribution
        self._sum_of_squares_1 += new_sample_1**2 - old_sample_1**2
        self._sum_of_squares_2 += new_sample_2**2 - old_sample_2**2

        # Replace the old sample with the new one in the buffer
        self._channel_one_samples[oldest_sample_index] = new_sample_1
        self._channel_two_samples[oldest_sample_index] = new_sample_2

        # Update the index
        self._channel_index = (self._channel_index + 1) % _SAMPLE_BUFFER_SIZE

        # Track the number of valid samples collected (up to the buffer size)
        if self._samples_collected < _SAMPLE_BUFFER_SIZE:
            self._samples_collected += 1

    def get_rms(self) -> list[float]:
        """
        Get the current RMS values for both channels.

        :returns: A list of two RMS values [RMS_channel_1, RMS_channel_2].
        """
        if self._samples_collected < _SAMPLE_BUFFER_SIZE:
            return [0.0, 0.0]

        # Calculate RMS using the valid number of samples
        rms_value_1: float = sqrt(self._sum_of_squares_1 / self._samples_collected)
        rms_value_2: float = sqrt(self._sum_of_squares_2 / self._samples_collected)

        return [rms_value_1, rms_value_2]
