# import analogio
import displayio
from adafruit_display_text import label

from . import colors as COLORS
from .battery_info import BatteryInfo
from .helper import FONT

# Not sure if i should show the battery percentage or icon
_SHOW_BATTERY_ICON = True

# _VOLTAGE_DIVIDER_CIRCUIT = False


# def _get_battery_percentage(voltage: float):
#     # Clamp the voltage between min and max to avoid percentages < 0 or > 100
#     voltage = max(min(voltage, BATTERY_MAX_VOLTAGE), BATTERY_MIN_VOLTAGE)
#     return (
#         (voltage - BATTERY_MIN_VOLTAGE)
#         / (BATTERY_MAX_VOLTAGE - BATTERY_MIN_VOLTAGE)
#         * 100
#     )


class BatteryIcon(displayio.Group):
    def __init__(self, battery_info: BatteryInfo, x: int, y: int) -> None:
        super().__init__()

        # self._vbat_voltage = analogio.AnalogIn(BATTERY_VOLTAGE_PIN)
        self._battery_info = battery_info

        if _SHOW_BATTERY_ICON:
            self._battery_icon_group = displayio.Group()
            terminal_bitmap = displayio.Bitmap(2, 4, 1)
            battery_terminal = displayio.TileGrid(
                terminal_bitmap, pixel_shader=COLORS.PALETTE_WHITE, x=x - 2, y=y + 2
            )

            battery_body_width = 21
            battery_body_bitmap = displayio.Bitmap(battery_body_width, 8, 1)
            battery_body = displayio.TileGrid(
                battery_body_bitmap, pixel_shader=COLORS.PALETTE_WHITE, x=x, y=y
            )

            self._battery_icon_group.append(battery_terminal)
            self._battery_icon_group.append(battery_body)

            num_of_segments = 4
            segment_width = int(battery_body_width / num_of_segments) - 1
            battery_block_bitmap = displayio.Bitmap(segment_width, 6, 1)
            block_x = x + 1
            self._battery_blocks = []
            for i in range(num_of_segments):
                self._battery_blocks.append(
                    displayio.TileGrid(
                        battery_block_bitmap,
                        pixel_shader=COLORS.PALETTE_BLACK,
                        x=(block_x + (segment_width * i)) + i,
                        y=y + 1,
                    )
                )
                self._battery_blocks[i].hidden = True
                self._battery_icon_group.append(self._battery_blocks[i])
        else:
            self._text_battery_percent = label.Label(FONT, x=x, y=y + 4)
            self._battery_icon_group.append(self._text_battery_percent)

        self._text_usb = label.Label(FONT, text="USB", x=x, y=y + 4)
        self._text_usb.hidden = True
        self.append(self._text_usb)
        self.append(self._battery_icon_group)

    def update(self) -> None:
        """Update the the battery icon"""
        if self._battery_info.is_usb_connected:
            self._battery_icon_group.hidden = True
            self._text_usb.hidden = False
            # self._text_usb.text = f"{self._battery_info.charge_rate}%"
        else:
            self._battery_icon_group.hidden = False
            self._text_usb.hidden = True
            battery_percent = self._battery_info.battery_percent
            # battery_percent = _get_battery_percentage(self.voltage)

            if _SHOW_BATTERY_ICON:
                self._battery_blocks[0].hidden = battery_percent < 80.0
                self._battery_blocks[1].hidden = battery_percent < 40.0
                self._battery_blocks[2].hidden = battery_percent < 20.0
                self._battery_blocks[3].hidden = battery_percent < 10.0
            else:
                self._text_battery_percent.text = f"{int(battery_percent)}%"

    # def _get_voltage(self) -> float:
    #     """Gets current battery voltage for voltage divider circuit"""
    #     return self._vbat_voltage.value / MAX_INT_16 * REFERENCE_VOLTAGE * 2.0
