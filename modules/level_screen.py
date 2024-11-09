import displayio
from vectorio import Polygon
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

        # The raw x and y value from the sensor
        self._text_level_x_y = label.Label(FONT, color=WHITE, x=0, y=8)
        self.level_group.append(self._text_level_x_y)

        # Box that show the status of the leveling
        box_width = int(CIRCUITPY_DISPLAY_WIDTH / 3)
        box_height = int(CIRCUITPY_DISPLAY_HEIGHT / 3)
        color_bitmap = displayio.Bitmap(box_width, box_height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = WHITE

        bg_sprite = displayio.TileGrid(
            color_bitmap, pixel_shader=color_palette, x=box_width, y=box_height
        )
        self.level_group.append(bg_sprite)

        border: int = 2
        inner_bitmap = displayio.Bitmap(box_width - border, box_height - border, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = BLACK
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=box_width + 1, y=box_height + 1
        )
        self.level_group.append(inner_sprite)

        # Some triangles to help move you in the right direction
        north_triangle_points = [
            (box_width + int(box_width / 2), box_height + int(box_height / 2)),
            (box_width, box_height),
            (box_width + box_width, box_height),
        ]

        east_triangle_points = [
            (box_width + box_width, box_height),
            (box_width + int(box_width / 2), box_height + int(box_height / 2)),
            (box_width + box_width, box_height + box_height),
        ]

        south_triangle_points = [
            (box_width + int(box_width / 2), box_height + int(box_height / 2)),
            (box_width, box_height + box_height),
            (box_width + box_width, box_height + box_height),
        ]

        west_triangle_points = [
            (box_width, box_height),
            (box_width + int(box_width / 2), box_height + int(box_height / 2)),
            (box_width, box_height + box_height),
        ]

        self._north_triangle = Polygon(
            pixel_shader=color_palette, points=north_triangle_points, x=0, y=0
        )
        self._east_triangle = Polygon(
            pixel_shader=color_palette, points=east_triangle_points, x=0, y=0
        )
        self._south_triangle = Polygon(
            pixel_shader=color_palette, points=south_triangle_points, x=0, y=0
        )
        self._west_triangle = Polygon(
            pixel_shader=color_palette, points=west_triangle_points, x=0, y=0
        )

        self._north_triangle.hidden = True
        self._east_triangle.hidden = True
        self._south_triangle.hidden = True
        self._west_triangle.hidden = True

        self.level_group.append(self._north_triangle)
        self.level_group.append(self._east_triangle)
        self.level_group.append(self._south_triangle)
        self.level_group.append(self._west_triangle)

        # if you can read this then you are good to go!
        text_leveled = label.Label(
            FONT,
            text="level",
            color=BLACK,
            x=box_width + 7,
            y=box_height + int(box_height / 2),
        )

        self.level_group.append(text_leveled)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the leveling tool"""
        screen.set_display(self.level_group)

    def update(self, x: float, y: float) -> None:
        """This update the x and y values on the display"""
        self._text_level_x_y.text = f"X: {x:.2f} Y: {y:.2f}"

        self._north_triangle.hidden = y >= 0
        self._east_triangle.hidden = x <= 0
        self._south_triangle.hidden = y <= 0
        self._west_triangle.hidden = x >= 0
