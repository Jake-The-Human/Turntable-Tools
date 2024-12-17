"""RP2040 ADC data capture happens here"""

from math import sqrt
from analogio import AnalogIn

from turntable_tools.helper import LEFT_CH_PIN, RIGHT_CH_PIN, MAX_INT_16


_SAMPLE_BUFFER_SIZE: int = 128


def _value_to_voltage(value: int, voltage_ref: float) -> float:
    """Change raw value to voltage and subtract the DC offset"""
    return ((value / MAX_INT_16) * voltage_ref) - (voltage_ref / 2.0)


class AdcSensor:
    def __init__(self) -> None:
        self.chan_L = AnalogIn(LEFT_CH_PIN)
        self.chan_R = AnalogIn(RIGHT_CH_PIN)

        # RMS
        self._channel_index: int = 0
        self._channel_L_samples: list[float] = [0.0] * _SAMPLE_BUFFER_SIZE
        self._channel_R_samples: list[float] = [0.0] * _SAMPLE_BUFFER_SIZE
        self._sum_of_squares_L: float = 0.0
        self._sum_of_squares_R: float = 0.0
        self._samples_collected: int = 0

    def update(self) -> None:
        """Update the buffer with new samples and maintain a running RMS."""
        new_sample_L: float = _value_to_voltage(
            self.chan_L.value, self.chan_L.reference_voltage
        )
        new_sample_R: float = _value_to_voltage(
            self.chan_R.value, self.chan_R.reference_voltage
        )

        # Get the index of the sample to be replaced
        oldest_sample_index: int = self._channel_index
        old_sample_L = self._channel_L_samples[oldest_sample_index]
        old_sample_R = self._channel_R_samples[oldest_sample_index]

        # Update the sum of squares by removing the old sample contribution
        self._sum_of_squares_L += new_sample_L**2 - old_sample_L**2
        self._sum_of_squares_R += new_sample_R**2 - old_sample_R**2

        # Replace the old sample with the new one in the buffer
        self._channel_L_samples[oldest_sample_index] = new_sample_L
        self._channel_R_samples[oldest_sample_index] = new_sample_R

        # Update the index
        self._channel_index = (self._channel_index + 1) % _SAMPLE_BUFFER_SIZE

        # Track the number of valid samples collected (up to the buffer size)
        if self._samples_collected < _SAMPLE_BUFFER_SIZE:
            self._samples_collected += 1

    def clear(self) -> None:
        """Resets member data to help make new measurements better"""
        self._channel_index = 0
        self._channel_L_samples = [0.0] * _SAMPLE_BUFFER_SIZE
        self._channel_R_samples = [0.0] * _SAMPLE_BUFFER_SIZE
        self._sum_of_squares_L = 0.0
        self._sum_of_squares_R = 0.0
        self._samples_collected = 0

    def get_rms(self) -> list[float]:
        """
        Get the current RMS values for both channels.

        :returns: A list of two RMS values [RMS_channel_1, RMS_channel_2].
        """
        if self._samples_collected == 0:
            return [0.0, 0.0]

        # Calculate RMS using the valid number of samples
        rms_value_L: float = sqrt(self._sum_of_squares_L / self._samples_collected)
        rms_value_R: float = sqrt(self._sum_of_squares_R / self._samples_collected)

        return [rms_value_L, rms_value_R]
