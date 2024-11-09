import displayio
from adafruit_display_text import label

import terminalio


class LevelingScreen:
    def __init__(self) -> None:
        self.level_group = displayio.Group(scale=2)
        self._text_level_x = label.Label(
            terminalio.FONT, text="", color=0xFFFFFF, x=0, y=8
        )
        self._text_level_y = label.Label(
            terminalio.FONT, text="", color=0xFFFFFF, x=0, y=16
        )
        self.level_group.append(self._text_level_x)
        self.level_group.append(self._text_level_y)

    def update(self, x: float, y: float) -> None:
        self._text_level_x.text = f"{x:.2f}"
        self._text_level_y.text = f"{y:.2f}"

    def get_group(self) -> displayio.Group:
        return self.level_group
