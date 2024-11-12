import displayio
from adafruit_display_text import label

from .display import Display
from .battery_status import BatteryStatus
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
        self._battery_status = BatteryStatus(CIRCUITPY_DISPLAY_WIDTH - 24, 4)
        title_group.append(text_title)
        title_group.append(self._battery_status.get_group())
        title_group.append(separator)

        menu_group = displayio.Group()
        self._menu_options = []

        for i, entry in enumerate(
            [STRINGS.RPM, STRINGS.LEVEL, STRINGS.RUMBLE, STRINGS.AZIMUTH]
        ):
            self._menu_options.append(
                label.Label(
                    FONT,
                    text=entry,
                    color=DisplayColor.WHITE,
                    padding_left=1,
                    padding_right=CIRCUITPY_DISPLAY_WIDTH,
                )
            )
            self._menu_options[i].x = 1
            self._menu_options[i].y = 22 + (self._menu_options[i].height * i)
            menu_group.append(self._menu_options[i])

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

        self._battery_status.update(100)
