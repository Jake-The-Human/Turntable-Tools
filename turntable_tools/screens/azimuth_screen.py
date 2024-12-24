import displayio

from adafruit_display_text import label
from turntable_tools.modes.azimuth_mode import AzimuthMode
from turntable_tools import colors as COLORS
from turntable_tools import strings as STRINGS
from turntable_tools.helper import FONT


class AzimuthScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()

        self._crosstalk_text = label.Label(
            FONT,
            color=COLORS.DISPLAY_WHITE,
            background_color=COLORS.DISPLAY_BLACK,
            padding_left=1,
            x=0,
            y=8,
        )

        self._crosstalk_value_text = label.Label(
            FONT,
            color=COLORS.DISPLAY_WHITE,
            background_color=COLORS.DISPLAY_BLACK,
            padding_left=1,
            x=0,
            y=20,
        )

        self.append(self._crosstalk_text)
        self.append(self._crosstalk_value_text)

    def update(self, azimuth_mode: AzimuthMode) -> None:
        """Update the rms voltage and crosstalk"""

        if azimuth_mode.crosstalk_left < 0.0:
            channel: str = "L"
            rms: float = azimuth_mode.rms_left
            crosstalk: float = azimuth_mode.crosstalk_left
        else:
            channel: str = "R"
            rms: float = azimuth_mode.rms_right
            crosstalk: float = azimuth_mode.crosstalk_right

        self._crosstalk_text.text = (
            f"{STRINGS.ALIGNMENT}: {AzimuthScreen._alignment(crosstalk)}."
        )

        self._crosstalk_value_text.text = f"{channel}: {rms:.2f}mV, {crosstalk:.2f}dB"

    @staticmethod
    def _alignment(crosstalk_db: float) -> str:
        quality: str = STRINGS.POOR
        if crosstalk_db < -30.0:
            quality = STRINGS.EXCELLENT
        elif crosstalk_db < -25.0:
            quality = STRINGS.GREAT
        elif crosstalk_db < -20.0:
            quality = STRINGS.GOOD

        return quality
