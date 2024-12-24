from math import log
from neopixel import NeoPixel

from turntable_tools.sensors.adc_sensor import AdcSensor
from turntable_tools.moving_average import MovingAvg
from turntable_tools.buttons import Buttons


def _crosstalk_to_db(main_signal: float, secondary_signal: float) -> float:
    """Converts the to signals that are in mV to a dB"""
    return 20.0 * log(secondary_signal / main_signal, 10) if main_signal != 0.0 else 0.0


class AzimuthMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel: NeoPixel = pixel
        self.rms_left: float = 0.0
        self.rms_right: float = 0.0
        self.crosstalk_left: float = 0.0
        self.crosstalk_right: float = 0.0
        self.crosstalk_avg_left = MovingAvg()
        self.crosstalk_avg_right = MovingAvg()
        self._freeze_crosstalk: bool = False

    def handle_buttons(self, buttons: Buttons) -> None:
        """Any mode specific action that are triggered by a button"""
        self._freeze_crosstalk = buttons.b_pressed

        if buttons.c_pressed or buttons.a_pressed:
            self.crosstalk_avg_left.clear()
            self.crosstalk_avg_right.clear()
            self.crosstalk_left = 0.0
            self.crosstalk_right = 0.0

    def update(self, adc_sensor: AdcSensor) -> None:
        """Update the buffer with new samples and maintain a running RMS and crosstalk."""
        self.rms_left, self.rms_right = adc_sensor.get_rms()

        if not self._freeze_crosstalk:
            self.crosstalk_left = self.crosstalk_avg_left.update(
                _crosstalk_to_db(self.rms_left, self.rms_right)
            )
            self.crosstalk_right = self.crosstalk_avg_right.update(
                _crosstalk_to_db(self.rms_right, self.rms_left)
            )
