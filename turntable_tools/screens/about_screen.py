"""This file is about the about page on the device

Source Code: https://github.com/Jake-The-Human/Turntable-Tools
"""

import displayio
from adafruit_display_text import label

from turntable_tools import colors as COLORS
from turntable_tools.helper import FONT


class AboutScreen(displayio.Group):
    """The about screen"""

    def __init__(self) -> None:
        super().__init__()
        _text_about = label.Label(
            FONT,
            text="Author: Jake Adamson\nMade in Boston MA B^)"
            "\nGitHub: Jake-The-\nHuman/Turntable-Tools",
            color=COLORS.DISPLAY_WHITE,
            x=2,
            y=8,
        )
        self.append(_text_about)
