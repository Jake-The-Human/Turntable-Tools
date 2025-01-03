"""
Turntable Tools - Easy to use tools for turntable measurement and control.

Filename: update_gui.py
Description: The purpose of this class is to separate the data collection from the screen updating.

Author: Jake-The-Human
Repository: https://github.com/Jake-The-Human/Turntable-Tools
License: GPL-3.0-or-later (see LICENSE file for details)
Date Created: 2024-12-17

This file is part of Turntable Tools.

Turntable Tools is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Turntable Tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Turntable Tools. If not, see <https://www.gnu.org/licenses/>.
"""

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
