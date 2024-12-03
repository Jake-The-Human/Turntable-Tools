import displayio
from .azimuth_mode import AzimuthMode
from adafruit_display_text import label
from .helper import FONT, DisplayColor


class AzimuthScreen(displayio.Group):
    def __init__(self) -> None:
        super().__init__()
        self._test = label.Label(
            FONT,
            color=DisplayColor.WHITE,
            background_color=DisplayColor.BLACK,
            padding_left=1,
            x=0,
            y=8,
        )
        self.append(self._test)

    def update(self, azimuth_mode: AzimuthMode) -> None:
        self._test.text = f"{azimuth_mode.rms_1:.3f}, {azimuth_mode.rms_2:.3f}"
