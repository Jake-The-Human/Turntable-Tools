import displayio
from adafruit_display_text import label

from .display import Display
from .helper import FONT, DisplayColor


class RumbleScreen:
    def __init__(self) -> None:
        self._rumble_group = displayio.Group()
        text_rumble = label.Label(
            FONT, color=DisplayColor.WHITE, text="Rumble coming soon!", y=8
        )
        self._rumble_group.append(text_rumble)

    def show_screen(self, screen: Display) -> None:
        """This will make the display rumble screen"""
        screen.set_display(self._rumble_group)

    def update(self) -> None:
        pass
