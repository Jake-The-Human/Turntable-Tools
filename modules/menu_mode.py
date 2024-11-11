from .helper import Mode


class MenuMode:
    def __init__(self):
        self._menu_index = 0

    def select(self) -> int:
        """Return the current index"""
        return self._menu_index

    def up(self) -> int:
        """Move the menu index up"""
        self._menu_index = (self._menu_index - 1) % Mode.SELECTABLE_MODES
        return self._menu_index

    def down(self) -> int:
        """Move the menu index down"""
        self._menu_index = (self._menu_index + 1) % Mode.SELECTABLE_MODES
        return self._menu_index
