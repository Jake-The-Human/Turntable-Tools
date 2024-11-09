import displayio
from adafruit_display_text import label

from .display import Display
from .helper import WHITE, FONT


class LevelScreen:
    def __init__(self) -> None:
        self.level_group = displayio.Group()
        self._text_level_x = label.Label(FONT, color=WHITE, x=0, y=8)
        self._text_level_y = label.Label(FONT, color=WHITE, x=0, y=16)
        self.level_group.append(self._text_level_x)
        self.level_group.append(self._text_level_y)

    def show_screen(self, screen: Display) -> None:
        screen.set_display(self.level_group)

    def update(self, x: float, y: float) -> None:
        self._text_level_x.text = f"{x:.2f}x"
        self._text_level_y.text = f"{y:.2f}y"
