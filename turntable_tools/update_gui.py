"""The purpose of this class is to separate the data collection from the screen updating"""

from time import time


class UpdateGui:
    """The purpose of this class is to separate the data collection from the screen updating"""

    def __init__(self) -> None:
        self.gui_update_time: float = 0.03
        self.timer: float = time()
        self.callback = UpdateGui._stub

    def update(self) -> None:
        """Check if enough time has pass before updating the gui"""
        if time() - self.timer >= self.gui_update_time:
            self.callback()
            self.timer = time()

    @staticmethod
    def _stub() -> None:
        pass
