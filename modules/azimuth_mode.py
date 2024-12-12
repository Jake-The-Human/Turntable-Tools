from math import log
from neopixel import NeoPixel
from modules.adc_sensor import AdcSensor
from.moving_average import MovingAvg
from .buttons import Buttons


def _crosstalk_to_db(main_signal: float, secondary_signal: float) -> float:
    """Converts the to signals that are in mV to a dB"""
    return 20.0 * log(secondary_signal / main_signal, 10) if main_signal != 0.0 else 0.0


class AzimuthMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel: NeoPixel = pixel
        self.rms_L: float = 0.0
        self.rms_R: float = 0.0
        self.crosstalk_L: float = 0.0
        self.crosstalk_R: float = 0.0
        self.crosstalk_avg_L = MovingAvg()
        self.crosstalk_avg_R = MovingAvg()
        self._freeze_crosstalk: bool = False

    def handle_buttons(self, buttons: Buttons) -> None:
        """Any mode specific action that are triggered by a button"""
        self._freeze_crosstalk = buttons.b_pressed()

        if buttons.c_pressed() or buttons.a_pressed():
            self.crosstalk_avg_L.clear()
            self.crosstalk_avg_R.clear()
            self.crosstalk_L = 0.0
            self.crosstalk_R = 0.0

    def update(self, adc_sensor: AdcSensor) -> None:
        """Update the buffer with new samples and maintain a running RMS and crosstalk."""
        self.rms_L, self.rms_R = adc_sensor.get_rms()

        if not self._freeze_crosstalk:
            self.crosstalk_L = self.crosstalk_avg_L.update(_crosstalk_to_db(self.rms_L, self.rms_R))
            self.crosstalk_R = self.crosstalk_avg_R.update(_crosstalk_to_db(self.rms_R, self.rms_L))
