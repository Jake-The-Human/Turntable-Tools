import displayio
from adafruit_display_text import label

import terminalio

RPM = "RPM, Wow & Flutter"
LEVEL = "Level"
RUMBLE = "Rumble"


class MainScreen:
    def __init__(self, screen_width: int) -> None:
        # Make the display context
        self.splash = displayio.Group()

        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        # Temp Main Menu elements
        title_group = displayio.Group(x=2, y=0)
        text_title = label.Label(
            terminalio.FONT, text="Turntable Tool", color=0xFFFFFF, x=2, y=8
        )
        sm_bitmap = displayio.Bitmap(screen_width, 1, 1)
        seperator = displayio.TileGrid(sm_bitmap, pixel_shader=color_palette, x=0, y=14)
        title_group.append(text_title)
        title_group.append(seperator)

        menu_group = displayio.Group(x=2, y=12)
        menu_x, menu_y = (2, 8)
        text_offset = 12
        text_menu_rmp = label.Label(
            terminalio.FONT, text=RPM, color=0xFFFFFF, x=menu_x, y=menu_y
        )
        menu_y += text_offset
        text_menu_level = label.Label(
            terminalio.FONT, text=LEVEL, color=0xFFFFFF, x=menu_x, y=menu_y
        )
        menu_y += text_offset
        text_menu_rumble = label.Label(
            terminalio.FONT, text=RUMBLE, color=0xFFFFFF, x=menu_x, y=menu_y
        )

        for menu_item in [
            text_menu_rmp,
            text_menu_level,
            text_menu_rumble,
        ]:
            menu_group.append(menu_item)

        self.splash.append(title_group)
        self.splash.append(menu_group)

    def get_group(self) -> displayio.Group:
        return self.splash
