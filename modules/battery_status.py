import displayio

from .helper import DisplayColor


class BatteryStatus:
    def __init__(self, x: int, y: int) -> None:
        self._battery_group = displayio.Group()
        color_palette = displayio.Palette(1)
        color_palette[0] = DisplayColor.WHITE

        terminal_bitmap = displayio.Bitmap(2, 4, 1)
        battery_terminal = displayio.TileGrid(
            terminal_bitmap, pixel_shader=color_palette, x=x - 2, y=y + 2
        )

        battery_body_bitmap = displayio.Bitmap(21, 8, 1)
        battery_body = displayio.TileGrid(
            battery_body_bitmap, pixel_shader=color_palette, x=x, y=y
        )

        temp = displayio.Palette(1)
        temp[0] = DisplayColor.BLACK

        segment_width = int(21 / 4) - 1
        battery_block_bitmap = displayio.Bitmap(segment_width, 6, 1)
        block_x = x + 1
        self._battery_blocks = []
        for i in range(4):
            self._battery_blocks.append(
                displayio.TileGrid(
                    battery_block_bitmap,
                    pixel_shader=temp,
                    x=(block_x + (segment_width * i)) + i,
                    y=y + 1,
                )
            )

        self._battery_group.append(battery_terminal)
        self._battery_group.append(battery_body)
        for segment in self._battery_blocks:
            self._battery_group.append(segment)

    def get_group(self) -> displayio.Group:
        return self._battery_group

    def update(self, battery_percent: float) -> None:
        self._battery_blocks[0].hidden = battery_percent < 80.0
        self._battery_blocks[1].hidden = battery_percent < 40.0
        self._battery_blocks[2].hidden = battery_percent < 20.0
        self._battery_blocks[3].hidden = battery_percent < 10.0
