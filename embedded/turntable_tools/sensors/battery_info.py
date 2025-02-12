"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: battery_info.py
Description: Logic for measuring battery status.

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

from busio import I2C
import adafruit_max1704x


class BatteryInfo:
    """
    A utility class for monitoring battery status using the MAX17048 sensor.

    This class provides methods to retrieve real-time information about the battery,
    such as voltage, charge rate, and state of charge percentage. It can also detect
    whether the device is connected to a USB power source.
    """

    def __init__(self, i2c: I2C):
        """
        Initializes the BatteryInfo class with the MAX17048 sensor.

        :param i2c: The I2C bus instance used for communication with the MAX17048 sensor.
        """
        self._max17 = adafruit_max1704x.MAX17048(i2c)

    @property
    def is_usb_connected(self) -> bool:
        """
        Checks if the device is connected to a USB power source.

        USB connection is inferred by checking if the battery voltage is 4.0V or higher
        and if the charge rate exceeds 0.5C.

        :return: True if a USB power source is detected; otherwise, False.
        """
        return self.voltage >= 4.0 and self.charge_rate > 0.5

    @property
    def voltage(self) -> float:
        """
        Retrieves the current cell voltage of the battery.

        The cell voltage is measured directly by the MAX17048 sensor.

        :return: The battery cell voltage in volts (V).
        """
        return self._max17.cell_voltage

    @property
    def charge_rate(self) -> float:
        """
        Retrieves the current charge rate of the battery.

        The charge rate represents the current (in amps) flowing into the battery
        during charging. A positive value indicates charging, while a negative value
        may indicate discharging.

        :return: The charge rate in amps (A).
        """
        return self._max17.charge_rate

    @property
    def battery_percent(self) -> float:
        """
        Retrieves the current state of charge (SOC) percentage of the battery.

        The SOC is calculated by the MAX17048 sensor and represents the remaining
        battery capacity as a percentage. The value is clamped to a maximum of 100%.

        :return: The state of charge as a percentage (0-100%).
        """
        return min(self._max17.cell_percent, 100.0)
