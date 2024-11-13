import displayio
from adafruit_display_text import label

from .helper import DisplayColor, FONT, CIRCUITPY_DISPLAY_WIDTH


class Menu:
    def __init__(
        self, items: list[str], visible_items: int = 1, x: int = 0, y: int = 0
    ) -> None:
        self.menu_items_names: list[str] = items
        self.group = displayio.Group(x=x, y=y)
        self._menu_items: list[label.Label] = []
        for i in range(visible_items):
            new_item = label.Label(
                FONT,
                text=items[i],
                color=DisplayColor.WHITE,
                padding_left=2,
                padding_right=CIRCUITPY_DISPLAY_WIDTH,
            )
            new_item.y = new_item.height * i
            self._menu_items.append(new_item)
            self.group.append(new_item)

        self._item_index: int = 0
        self._menu_index: int = 0
        self._prev_index: int = -1

        self._menu_items[self._menu_index].background_color = DisplayColor.WHITE
        self._menu_items[self._menu_index].color = DisplayColor.BLACK

        self._update()

    def __len__(self):
        return len(self._menu_items)

    def select(self) -> int:
        """Return the current index"""
        return self._item_index

    def up(self) -> None:
        """Move the menu index up"""
        self._item_index = (self._item_index - 1) % len(self.menu_items_names)
        self._menu_index = (self._menu_index - 1) % len(self._menu_items)
        self._update()

    def down(self) -> None:
        """Move the menu index down"""
        self._item_index = (self._item_index + 1) % len(self.menu_items_names)
        self._menu_index = (self._menu_index + 1) % len(self._menu_items)
        self._update()

    def get_item(self, index: int) -> label.Label:
        """Get menu item at that index"""
        return self._menu_items[index]

    def _update(self) -> None:
        if not self._menu_items:
            return

        top_index = self._item_index
        bottom_index = top_index + (len(self._menu_items))
        for i, item in enumerate(range(self._item_index, bottom_index)):
            if item < len(self.menu_items_names):
                self._menu_items[i].text = self.menu_items_names[item]
            else:
                self._menu_items[i].text = ""

        # self._menu_items[self._menu_index].background_color = DisplayColor.WHITE
        # self._menu_items[self._menu_index].color = DisplayColor.BLACK

        # if self._prev_index >= 0:
        #     self._menu_items[self._prev_index].background_color = None
        #     self._menu_items[self._prev_index].color = DisplayColor.WHITE

        # self._prev_index = self._menu_index
