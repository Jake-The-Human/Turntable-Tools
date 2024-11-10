"""This file is the entry point for the Turntable Tool"""

import time
import board

import neopixel

# import busio
# import digitalio
# import storage
# import adafruit_sdcard

from modules.helper import Mode, PixelColor
from modules.display import Display
from modules.mems_sensor import MemsSensor
from modules.rpm_mode import RPMMode
from modules.level_mode import LevelMode
from modules.rumble_mode import RumbleMode
from modules.main_screen import MainScreen
from modules.rpm_screen import RPMScreen
from modules.level_screen import LevelScreen
from modules.rumble_screen import RumbleScreen

# Connect to the card and mount the filesystem.
# cs = digitalio.DigitalInOut(board.SD_CS)
# sd_spi = busio.SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
# sdcard = adafruit_sdcard.SDCard(sd_spi, cs)
# vfs = storage.VfsFat(sdcard)
# storage.mount(vfs, "/sd")

# Setup Feather board
i2c = board.STEMMA_I2C()
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 1.0
sensor = MemsSensor(i2c)
screen = Display(board.I2C())

# Setup the different tools
rpm_mode = RPMMode(pixel)
level_mode = LevelMode(pixel)
rumble_mode = RumbleMode()

# Setup the display logic for the different tools
main_screen = MainScreen()
rpm_screen = RPMScreen()
level_screen = LevelScreen()
rumble_screen = RumbleScreen()

# Init start up state
main_screen.show_screen(screen)
mode = Mode.MAIN_MENU
timer: float = 0


def update_gui(current_mode: int, new_mode: int) -> int:
    """This function handles update the gui's mode"""
    if new_mode == current_mode:
        return current_mode

    if new_mode == Mode.MAIN_MENU:
        main_screen.show_screen(screen)
    elif new_mode == Mode.RPM:
        rpm_screen.show_screen(screen)
    elif new_mode == Mode.LEVEL:
        level_screen.show_screen(screen)
    elif new_mode == Mode.RUMBLE:
        rumble_screen.show_screen(screen)

    time.sleep(0.2)
    return new_mode


# Main logic loop
while True:
    sensor.update()

    btn_a, btn_b, btn_c = screen.check_buttons()

    if mode == Mode.MAIN_MENU:
        if btn_a:
            mode = update_gui(current_mode=mode, new_mode=Mode.RPM)
            sensor.set_offset()
        elif btn_b:
            mode = update_gui(current_mode=mode, new_mode=Mode.LEVEL)
        elif btn_c:
            mode = update_gui(current_mode=mode, new_mode=Mode.RUMBLE)
            sensor.set_offset()

        pixel.fill(PixelColor.OFF)

    elif mode == Mode.RPM:
        if btn_a:
            mode = update_gui(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif btn_b:
            # Start recording rpm data
            rpm_mode.start()

        elif btn_c:
            # This sleep is used to avoided capturing the button press
            time.sleep(0.7)
            sensor.set_offset()

        new_rpm = rpm_mode.update(sensor.get_rpm())
        rpm_screen.update(rpm_mode, new_rpm)

    elif mode == Mode.LEVEL:
        if btn_a:
            mode = update_gui(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif btn_b:
            pass
        elif btn_c:
            sensor.set_offset()

        new_x, new_y = level_mode.update(sensor.get_acceleration())
        level_screen.update(new_x, new_y)

    elif mode == Mode.RUMBLE:
        if btn_a:
            mode = update_gui(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif btn_b:
            pass
        elif btn_c:
            sensor.set_offset()

        rumble_mode.update()

    time.sleep(0.016)
