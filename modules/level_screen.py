import displayio
from adafruit_display_text import label

from .display import Display
from .helper import (
    WHITE,
    BLACK,
    FONT,
    CIRCUITPY_DISPLAY_WIDTH,
    CIRCUITPY_DISPLAY_HEIGHT,
)


class LevelScreen:
    def __init__(self) -> None:
        self.level_group = displayio.Group()
        self._text_level_x = label.Label(FONT, color=WHITE, x=0, y=8)
        self._text_level_y = label.Label(FONT, color=WHITE, x=0, y=16)
        self.level_group.append(self._text_level_x)
        self.level_group.append(self._text_level_y)

        box_width = int(CIRCUITPY_DISPLAY_WIDTH / 3)
        box_height = int(CIRCUITPY_DISPLAY_HEIGHT / 3)
        color_bitmap = displayio.Bitmap(box_width, box_height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = WHITE

        bg_sprite = displayio.TileGrid(
            color_bitmap, pixel_shader=color_palette, x=box_width, y=box_height
        )
        self.level_group.append(bg_sprite)

        # Draw a smaller inner rectangle in black
        border: int = 2
        inner_bitmap = displayio.Bitmap(box_width - border, box_height - border, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = BLACK
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=box_width + 1, y=box_height + 1
        )
        self.level_group.append(inner_sprite)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the leveling tool"""
        screen.set_display(self.level_group)

    def update(self, x: float, y: float) -> None:
        """This update the x and y values on the display"""
        self._text_level_x.text = f"{x:.2f}x"
        self._text_level_y.text = f"{y:.2f}y"
