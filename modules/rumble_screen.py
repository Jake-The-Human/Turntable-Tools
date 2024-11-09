import displayio
from adafruit_display_text import label

from .display import Display
from .helper import FONT, WHITE


class RumbleScreen:
    def __init__(self) -> None:
        self._rumble_group = displayio.Group()
        self._text_rumble = label.Label(
            FONT, color=WHITE, text="Rumble coming soon!", y=8
        )
        self._rumble_group.append(self._text_rumble)

    def show_screen(self, screen: Display) -> None:
        """This will make the display rumble screen"""
        screen.set_display(self._rumble_group)

    def update(self) -> None:
        pass
