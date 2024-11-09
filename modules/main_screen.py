import displayio
from adafruit_display_text import label

from .display import Display
from .helper import WHITE, FONT, STRINGS, CIRCUITPY_DISPLAY_WIDTH


class MainScreen:
    def __init__(self) -> None:
        # Make the display context
        self.splash = displayio.Group()

        color_palette = displayio.Palette(1)
        color_palette[0] = WHITE

        # Temp Main Menu elements
        title_group = displayio.Group(x=2, y=0)
        text_title = label.Label(FONT, text=STRINGS.TITLE, color=WHITE, x=2, y=8)
        sm_bitmap = displayio.Bitmap(CIRCUITPY_DISPLAY_WIDTH, 1, 1)
        separator = displayio.TileGrid(sm_bitmap, pixel_shader=color_palette, x=0, y=14)
        title_group.append(text_title)
        title_group.append(separator)

        menu_group = displayio.Group(x=2, y=12)
        menu_x, menu_y = (2, 8)
        text_offset = 12
        text_menu_rmp = label.Label(
            FONT, text=STRINGS.RPM_WOW, color=WHITE, x=menu_x, y=menu_y
        )
        menu_y += text_offset
        text_menu_level = label.Label(
            FONT, text=STRINGS.LEVEL, color=WHITE, x=menu_x, y=menu_y
        )
        menu_y += text_offset
        text_menu_rumble = label.Label(
            FONT, text=STRINGS.RUMBLE, color=WHITE, x=menu_x, y=menu_y
        )

        menu_group.append(text_menu_rmp)
        menu_group.append(text_menu_level)
        menu_group.append(text_menu_rumble)

        self.splash.append(title_group)
        self.splash.append(menu_group)

    def show_screen(self, screen: Display) -> None:
        """This will make the display show main menu"""
        screen.set_display(self.splash)
