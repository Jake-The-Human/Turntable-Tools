import displayio
from adafruit_display_text import label

import terminalio


class RPMScreen:
    def __init__(self) -> None:
        self.rpm_group = displayio.Group(scale=3)
        self._text_rpm = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=0, y=8)
        self.rpm_group.append(self._text_rpm)

    def update(self, rpm: float):
        self._text_rpm.text = f"{rpm:.2f}"

    def get_group(self) -> displayio.Group:
        return self.rpm_group
