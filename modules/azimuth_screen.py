import displayio
from adafruit_display_text import label
from .azimuth_mode import AzimuthMode
from .helper import FONT, DisplayColor


class AzimuthScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()
        self._channel_one_text = label.Label(
            FONT,
            color=DisplayColor.WHITE,
            background_color=DisplayColor.BLACK,
            padding_left=1,
            x=0,
            y=8,
        )

        self._channel_two_text = label.Label(
            FONT,
            color=DisplayColor.WHITE,
            background_color=DisplayColor.BLACK,
            padding_left=1,
            x=0,
            y=18,
        )

        self.append(self._channel_one_text)
        self.append(self._channel_two_text)

    def update(self, azimuth_mode: AzimuthMode) -> None:
        """Update the rms voltage and crosstalk"""
        self._channel_one_text.text = f"L: {azimuth_mode.rms_L:.2f}mV, {azimuth_mode.crosstalk_L:.2f}dB"
        self._channel_two_text.text = f"R: {azimuth_mode.rms_R:.2f}mV, {azimuth_mode.crosstalk_R:.2f}dB"
