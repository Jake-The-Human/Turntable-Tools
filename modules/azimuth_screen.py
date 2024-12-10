import displayio
from adafruit_display_text import label
from .azimuth_mode import AzimuthMode
from .helper import FONT, DisplayColor, STRINGS


class AzimuthScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()

        self._crosstalk_text = label.Label(
            FONT,
            color=DisplayColor.WHITE,
            background_color=DisplayColor.BLACK,
            padding_left=1,
            x=0,
            y=8,
        )

        self._crosstalk_value_text = label.Label(
            FONT,
            color=DisplayColor.WHITE,
            background_color=DisplayColor.BLACK,
            padding_left=1,
            x=0,
            y=20,
        )

        self.append(self._crosstalk_text)
        self.append(self._crosstalk_value_text)

    def update(self, azimuth_mode: AzimuthMode) -> None:
        """Update the rms voltage and crosstalk"""

        if azimuth_mode.crosstalk_L < 0.0:
            channel: str = "L"
            rms: float = azimuth_mode.rms_L
            crosstalk: float = azimuth_mode.crosstalk_L
        else:
            channel: str = "R"
            rms: float = azimuth_mode.rms_R
            crosstalk: float = azimuth_mode.crosstalk_R

        self._crosstalk_text.text = (
            f"{STRINGS.ALIGNMENT} is {AzimuthScreen._alignment(crosstalk)}."
        )

        self._crosstalk_value_text.text = f"{channel}: {rms:.2f}mV, {crosstalk:.2f}dB"

    @staticmethod
    def _alignment(crosstalk_db: float) -> str:
        quality: str = "poor"
        if crosstalk_db < -30.0:
            quality = "excellent"
        elif crosstalk_db < -25.0:
            quality = "great"
        elif crosstalk_db < -20.0:
            quality = "good"

        return quality
