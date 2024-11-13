import displayio
from adafruit_display_text import label

from .display import Display
from .helper import STRINGS, DisplayColor, FONT, HAS_AZIMUTH_CIRCUIT


class AzimuthScreen:
    def __init__(self) -> None:
        self._azimuth_group = displayio.Group()
        if not HAS_AZIMUTH_CIRCUIT:
            text_title = label.Label(
                FONT,
                text=STRINGS.NO_AZIMUTH,
                color=DisplayColor.WHITE,
                y=8,
                padding_left=2,
            )
            self._azimuth_group.append(text_title)
        else:
            pass

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the azimuth tool"""
        screen.set_display(self._azimuth_group)

    def update(self) -> None:
        pass
