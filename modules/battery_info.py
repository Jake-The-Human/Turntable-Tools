# from math import min
import adafruit_max1704x


class BatteryInfo:
    def __init__(self, i2c):
        self._max17 = adafruit_max1704x.MAX17048(i2c)

    def is_usb_connected(self) -> bool:
        return self.get_voltage() >= 4.0 and self.get_charge_rate() > 0.5

    def get_voltage(self) -> float:
        return self._max17.cell_voltage

    def get_charge_rate(self) -> float:
        return self._max17.charge_rate

    def get_percent(self) -> float:
        print(self._max17.cell_voltage)
        return min(self._max17.cell_percent, 100.0)
