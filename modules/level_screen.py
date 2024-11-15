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
    SHOW_X_Y,
)

_NORTH = 0
_EAST = 1
_SOUTH = 2
_WEST = 3


class LevelScreen:
    def __init__(self) -> None:
        self._level_group = displayio.Group()

        BORDER: int = 2
        # Box that show the status of the leveling
        box_width = CIRCUITPY_DISPLAY_WIDTH
        box_height = CIRCUITPY_DISPLAY_HEIGHT
        color_bitmap = displayio.Bitmap(box_width, box_height, 1)

        bg_sprite = displayio.TileGrid(
            color_bitmap, pixel_shader=WHITE_PALETTE, x=0, y=0
        )

        inner_bitmap = displayio.Bitmap(box_width - BORDER, box_height - BORDER, 1)

        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=BLACK_PALETTE, x=1, y=1
        )

        # Some triangles to help move you in the right direction
        top_left = (0, 0)
        top_right = (box_width, 0)
        center_point = (int(box_width / 2), int(box_height / 2))
        bottom_left = (0, box_height)
        bottom_right = (box_width, box_height)

        triangle_points = [
            [top_left, center_point, top_right],
            [top_right, center_point, bottom_right],
            [bottom_left, center_point, bottom_right],
            [top_left, center_point, bottom_left],
        ]

        self._triangles: list[Polygon] = [
            Polygon(pixel_shader=WHITE_PALETTE, points=triangle, x=0, y=0)
            for triangle in triangle_points
        ]

        # The raw x and y value from the sensor
        self._text_level_x_y = label.Label(
            FONT,
            color=DisplayColor.WHITE,
            background_color=DisplayColor.BLACK,
            padding_left=1,
            x=BORDER + 1,
            y=8 + 1,
        )

        # if you can read this then you are good to go!
        text_leveled = label.Label(
            FONT, text=STRINGS.LEVEL, color=DisplayColor.BLACK, scale=2
        )
        text_leveled.x = int(box_width / 2) - text_leveled.width
        text_leveled.y = int(box_height / 2)

        self._level_group.append(bg_sprite)
        self._level_group.append(inner_sprite)

        for triangle in self._triangles:
            triangle.hidden = True
            self._level_group.append(triangle)

        if SHOW_X_Y:
            self._level_group.append(self._text_level_x_y)

        self._level_group.append(text_leveled)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show the leveling tool"""
        screen.set_display(self._level_group)

    def update(self, sensor_data: tuple[float, float]) -> None:
        """This update the x and y values on the display"""
        x, y = sensor_data
        if SHOW_X_Y:
            self._text_level_x_y.text = f"X:{x:.2f} Y:{y:.2f}"

        self._triangles[_NORTH].hidden = y >= 0
        self._triangles[_EAST].hidden = x <= 0
        self._triangles[_SOUTH].hidden = y <= 0
        self._triangles[_WEST].hidden = x >= 0
