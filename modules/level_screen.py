import displayio
from vectorio import Polygon
from adafruit_display_text import label

from .display import Display
from .helper import (
    DisplayColor,
    STRINGS,
    FONT,
    CIRCUITPY_DISPLAY_WIDTH,
    CIRCUITPY_DISPLAY_HEIGHT,
    WHITE_PALETTE,
    BLACK_PALETTE,
)


class LevelScreen:
    def __init__(self) -> None:
        self._level_group = displayio.Group()

        # The raw x and y value from the sensor
        self._text_level_x_y = label.Label(FONT, color=DisplayColor.WHITE, x=0, y=8)
        self._level_group.append(self._text_level_x_y)

        # Box that show the status of the leveling
        box_width = int(CIRCUITPY_DISPLAY_WIDTH / 3)
        box_height = int(CIRCUITPY_DISPLAY_HEIGHT / 3)
        color_bitmap = displayio.Bitmap(box_width, box_height, 1)

        bg_sprite = displayio.TileGrid(
            color_bitmap, pixel_shader=WHITE_PALETTE, x=box_width, y=box_height
        )
        self._level_group.append(bg_sprite)

        border: int = 2
        inner_bitmap = displayio.Bitmap(box_width - border, box_height - border, 1)

        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=BLACK_PALETTE, x=box_width + 1, y=box_height + 1
        )
        self._level_group.append(inner_sprite)

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
            (box_width, box_height + box_height - 1),
            (box_width + box_width, box_height + box_height),
        ]

        west_triangle_points = [
            (box_width, box_height),
            (box_width + int(box_width / 2), box_height + int(box_height / 2)),
            (box_width, box_height + box_height),
        ]

        self._north_triangle = Polygon(
            pixel_shader=WHITE_PALETTE, points=north_triangle_points, x=0, y=0
        )
        self._east_triangle = Polygon(
            pixel_shader=WHITE_PALETTE, points=east_triangle_points, x=0, y=0
        )
        self._south_triangle = Polygon(
            pixel_shader=WHITE_PALETTE, points=south_triangle_points, x=0, y=0
        )
        self._west_triangle = Polygon(
            pixel_shader=WHITE_PALETTE, points=west_triangle_points, x=0, y=0
        )

        self._north_triangle.hidden = True
        self._east_triangle.hidden = True
        self._south_triangle.hidden = True
        self._west_triangle.hidden = True

        self._level_group.append(self._north_triangle)
        self._level_group.append(self._east_triangle)
        self._level_group.append(self._south_triangle)
        self._level_group.append(self._west_triangle)

        # if you can read this then you are good to go!
        text_leveled = label.Label(
            FONT,
            text=STRINGS.LEVEL,
            color=DisplayColor.BLACK,
            x=box_width + 7,
            y=box_height + int(box_height / 2),
        )

        self._level_group.append(text_leveled)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the leveling tool"""
        screen.set_display(self._level_group)

    def update(self, sensor_data: tuple[float, float]) -> None:
        """This update the x and y values on the display"""
        x, y = sensor_data
        self._text_level_x_y.text = f"X: {x:.2f} Y: {y:.2f}"

        self._north_triangle.hidden = y >= 0
        self._east_triangle.hidden = x <= 0
        self._south_triangle.hidden = y <= 0
        self._west_triangle.hidden = x >= 0
