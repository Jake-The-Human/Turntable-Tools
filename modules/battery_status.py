import analogio
import displayio
from adafruit_display_text import label

from .helper import (
    BATTERY_VOLTAGE_PIN,
    BATTERY_MIN_VOLTAGE,
    BATTERY_MAX_VOLTAGE,
    REFERENCE_VOLTAGE,
    WHITE_PALETTE,
    BLACK_PALETTE,
    FONT,
)

# Not sure if i should show the battery percentage or icon
_SHOW_BATTERY_ICON = True


def _get_battery_percentage(voltage: float):
    # Clamp the voltage between min and max to avoid percentages < 0 or > 100
    voltage = max(min(voltage, BATTERY_MAX_VOLTAGE), BATTERY_MIN_VOLTAGE)
    return (
        (voltage - BATTERY_MIN_VOLTAGE)
        / (BATTERY_MAX_VOLTAGE - BATTERY_MIN_VOLTAGE)
        * 100
    )


class BatteryStatus:
    def __init__(self, x: int, y: int) -> None:
        self._vbat_voltage = analogio.AnalogIn(BATTERY_VOLTAGE_PIN)

        self._battery_group = displayio.Group()
        if _SHOW_BATTERY_ICON:
            terminal_bitmap = displayio.Bitmap(2, 4, 1)
            battery_terminal = displayio.TileGrid(
                terminal_bitmap, pixel_shader=WHITE_PALETTE, x=x - 2, y=y + 2
            )

            battery_body_width = 21
            battery_body_bitmap = displayio.Bitmap(battery_body_width, 8, 1)
            battery_body = displayio.TileGrid(
                battery_body_bitmap, pixel_shader=WHITE_PALETTE, x=x, y=y
            )

            self._battery_group.append(battery_terminal)
            self._battery_group.append(battery_body)

            num_of_segments = 4
            segment_width = int(battery_body_width / num_of_segments) - 1
            battery_block_bitmap = displayio.Bitmap(segment_width, 6, 1)
            block_x = x + 1
            self._battery_blocks = []
            for i in range(num_of_segments):
                self._battery_blocks.append(
                    displayio.TileGrid(
                        battery_block_bitmap,
                        pixel_shader=BLACK_PALETTE,
                        x=(block_x + (segment_width * i)) + i,
                        y=y + 1,
                    )
                )
                self._battery_blocks[i].hidden = True
                self._battery_group.append(self._battery_blocks[i])
        else:
            self._text_battery_percent = label.Label(FONT, x=x, y=y + 4)
            self._battery_group.append(self._text_battery_percent)

    def get_group(self) -> displayio.Group:
        return self._battery_group

    def update(self) -> None:
        battery_percent = _get_battery_percentage(self._get_voltage())

        if _SHOW_BATTERY_ICON:
            self._battery_blocks[0].hidden = battery_percent < 80.0
            self._battery_blocks[1].hidden = battery_percent < 40.0
            self._battery_blocks[2].hidden = battery_percent < 20.0
            self._battery_blocks[3].hidden = battery_percent < 10.0
        else:
            self._text_battery_percent.text = f"{int(battery_percent)}%"

    def _get_voltage(self) -> float:
        """Gets current battery voltage"""
        return self._vbat_voltage.value / 65535.0 * REFERENCE_VOLTAGE * 2.0
