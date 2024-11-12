import displayio
from adafruit_display_text import label

from .display import Display
from .helper import DisplayColor, STRINGS, Mode, FONT, CIRCUITPY_DISPLAY_WIDTH


class MenuScreen:
    def __init__(self) -> None:
        self._prev_index = Mode.SELECTABLE_MODES - 1
        # Make the display context
        self._main_group = displayio.Group()

        color_palette = displayio.Palette(1)
        color_palette[0] = DisplayColor.WHITE

        # Temp Main Menu elements
        title_group = displayio.Group()
        text_title = label.Label(
            FONT, text=STRINGS.TITLE, color=DisplayColor.WHITE, x=0, y=8, padding_left=2
        )
        sm_bitmap = displayio.Bitmap(CIRCUITPY_DISPLAY_WIDTH, 1, 1)
        separator = displayio.TileGrid(sm_bitmap, pixel_shader=color_palette, x=0, y=14)
        title_group.append(text_title)
        title_group.append(separator)

        menu_group = displayio.Group(x=1, y=14)
        menu_y = 8
        text_y_offset = 12
        text_menu_rmp = label.Label(
            FONT,
            text=STRINGS.RPM_WOW,
            color=DisplayColor.WHITE,
            x=0,
            y=menu_y,
            padding_left=1,
            padding_right=CIRCUITPY_DISPLAY_WIDTH,
        )
        menu_y += text_y_offset
        text_menu_level = label.Label(
            FONT,
            text=STRINGS.LEVEL,
            color=DisplayColor.WHITE,
            x=0,
            y=menu_y,
            padding_left=1,
            padding_right=CIRCUITPY_DISPLAY_WIDTH,
        )
        menu_y += text_y_offset
        text_menu_rumble = label.Label(
            FONT,
            text=STRINGS.RUMBLE,
            color=DisplayColor.WHITE,
            x=0,
            y=menu_y,
            padding_left=1,
            padding_right=CIRCUITPY_DISPLAY_WIDTH,
        )
        menu_y += text_y_offset
        text_menu_azimuth = label.Label(
            FONT,
            text=STRINGS.AZIMUTH,
            color=DisplayColor.WHITE,
            x=0,
            y=menu_y,
            padding_left=1,
            padding_right=CIRCUITPY_DISPLAY_WIDTH,
        )

        self._menu_options = [
            text_menu_rmp,
            text_menu_level,
            text_menu_rumble,
            text_menu_azimuth,
        ]
        for entry in self._menu_options:
            menu_group.append(entry)

        self._main_group.append(title_group)
        self._main_group.append(menu_group)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show main menu"""
        screen.set_display(self._main_group)

    def update(self, menu_index: int) -> None:
        self._menu_options[menu_index].background_color = DisplayColor.WHITE
        self._menu_options[menu_index].color = DisplayColor.BLACK

        self._menu_options[self._prev_index].background_color = DisplayColor.BLACK
        self._menu_options[self._prev_index].color = DisplayColor.WHITE
        self._prev_index = menu_index
