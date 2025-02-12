"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: adc_sensor.py
Description: RP2040 ADC data capture happens here.

Author: Jake-The-Human
Repository: https://github.com/Jake-The-Human/Turntable-Tools
License: GPL-3.0-or-later (see LICENSE file for details)
Date Created: 2024-12-17

This file is part of Turntable Tools.

Turntable Tools is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Turntable Tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Turntable Tools. If not, see <https://www.gnu.org/licenses/>.
"""

from math import sqrt
from analogio import AnalogIn

from turntable_tools.helper import LEFT_CH_PIN, RIGHT_CH_PIN, MAX_INT_16


_SAMPLE_BUFFER_SIZE: int = 128


def _value_to_voltage(value: int, voltage_ref: float) -> float:
    """Change raw value to voltage and subtract the DC offset"""
    return ((value / MAX_INT_16) * voltage_ref) - (voltage_ref / 2.0)


class AdcSensor:
    def __init__(self) -> None:
        self.chan_left = AnalogIn(LEFT_CH_PIN)
        self.chan_right = AnalogIn(RIGHT_CH_PIN)

        # RMS
        self._channel_index: int = 0
        self._channel_left_samples: list[float] = [0.0] * _SAMPLE_BUFFER_SIZE
        self._channel_right_samples: list[float] = [0.0] * _SAMPLE_BUFFER_SIZE
        self._sum_of_squares_left: float = 0.0
        self._sum_of_squares_right: float = 0.0
        self._samples_collected: int = 0

    def update(self) -> None:
        """Update the buffer with new samples and maintain a running RMS."""
        new_sample_left: float = _value_to_voltage(
            self.chan_left.value, self.chan_left.reference_voltage
        )
        new_sample_right: float = _value_to_voltage(
            self.chan_right.value, self.chan_right.reference_voltage
        )

        # Get the index of the sample to be replaced
        oldest_sample_index: int = self._channel_index
        old_sample_left: float = self._channel_left_samples[oldest_sample_index]
        old_sample_right: float = self._channel_right_samples[oldest_sample_index]

        # Update the sum of squares by removing the old sample contribution
        self._sum_of_squares_left += new_sample_left**2 - old_sample_left**2
        self._sum_of_squares_right += new_sample_right**2 - old_sample_right**2

        # Replace the old sample with the new one in the buffer
        self._channel_left_samples[oldest_sample_index] = new_sample_left
        self._channel_right_samples[oldest_sample_index] = new_sample_right

        # Update the index
        self._channel_index = (self._channel_index + 1) % _SAMPLE_BUFFER_SIZE

        # Track the number of valid samples collected (up to the buffer size)
        if self._samples_collected < _SAMPLE_BUFFER_SIZE:
            self._samples_collected += 1

    def clear(self) -> None:
        """Resets member data to help make new measurements better"""
        self._channel_index = 0
        self._channel_left_samples = [0.0] * _SAMPLE_BUFFER_SIZE
        self._channel_right_samples = [0.0] * _SAMPLE_BUFFER_SIZE
        self._sum_of_squares_left = 0.0
        self._sum_of_squares_right = 0.0
        self._samples_collected = 0

    def get_rms(self) -> list[float]:
        """
        Get the current RMS values for both channels.

        :returns: A list of two RMS values [RMS_channel_1, RMS_channel_2].
        """
        sample_count: int = self._samples_collected

        if sample_count == 0:
            return [0.0, 0.0]

        # Calculate RMS using the valid number of samples
        rms_left: float = sqrt(self._sum_of_squares_left / sample_count)
        rms_right: float = sqrt(self._sum_of_squares_right / sample_count)

        return [rms_left, rms_right]
