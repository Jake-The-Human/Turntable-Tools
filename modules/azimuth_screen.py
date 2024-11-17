import displayio

from .display import Display


class AzimuthScreen:
    def __init__(self) -> None:
        self._azimuth_group = displayio.Group()

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the azimuth tool"""
        screen.set_display(self._azimuth_group)

    def update(self, _) -> None:
        pass
