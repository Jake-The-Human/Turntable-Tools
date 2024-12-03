"""This file is about the about page on the device"""

import displayio
from adafruit_display_text import label

from .helper import FONT, DisplayColor


class AboutScreen(displayio.Group):
    """The about screen"""

    def __init__(self) -> None:
        super().__init__()
        _text_about = label.Label(
            FONT,
            text="Author: Jake Adamson\nMade in Boston MA B^)"
            "\nGitHub: Jake-The-\nHuman/Turntable-Tools",
            color=DisplayColor.WHITE,
            x=2,
            y=8,
        )
        self.append(_text_about)
