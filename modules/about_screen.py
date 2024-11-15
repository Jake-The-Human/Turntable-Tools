"""This file is about the about page on the device"""

import displayio
from adafruit_display_text import label

from .display import Display
from .helper import FONT, DisplayColor


class AboutScreen:
    def __init__(self) -> None:
        self._about_group = displayio.Group()
        _text_about = label.Label(
            FONT,
            text="Author: Jake Adamson\nMade in Boston MA B^)"
            "\nGitHub: Jake-The-\nHuman/Turntable-Tools",
            color=DisplayColor.WHITE,
            x=2,
            y=8,
        )
        self._about_group.append(_text_about)

    def show_screen(self, screen: Display) -> None:
        """This will make the display about screen"""
        screen.set_display(self._about_group)
