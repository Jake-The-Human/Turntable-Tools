"""This file is the entry point for the Turntable Tool"""

import time
import board

import neopixel

from modules.helper import Mode, PixelColor, HAS_SD_CARD
from modules.display import Display
from modules.mems_sensor import MemsSensor
from modules.menu_mode import MenuMode
from modules.rpm_mode import RPMMode
from modules.level_mode import LevelMode
from modules.rumble_mode import RumbleMode
from modules.azimuth_mode import AzimuthMode
from modules.menu_screen import MenuScreen
from modules.rpm_screen import RPMScreen
from modules.level_screen import LevelScreen
from modules.rumble_screen import RumbleScreen
from modules.azimuth_screen import AzimuthScreen

if HAS_SD_CARD:
    import busio
    import digitalio
    import storage
    import adafruit_sdcard

    # Connect to the card and mount the filesystem.
    cs = digitalio.DigitalInOut(board.SD_CS)
    sd_spi = busio.SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
    sd_card = adafruit_sdcard.SDCard(sd_spi, cs)
    vfs = storage.VfsFat(sd_card)
    storage.mount(vfs, "/sd")

# Setup Feather board
i2c = board.STEMMA_I2C()
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
sensor = MemsSensor(i2c)
screen = Display(board.I2C())

# Setup the different tools
menu_mode = MenuMode()
rpm_mode = RPMMode(pixel)
level_mode = LevelMode(pixel)
rumble_mode = RumbleMode(pixel)
azimuth_mode = AzimuthMode(pixel)

# Setup the display logic for the different tools
main_screen = MenuScreen()
rpm_screen = RPMScreen()
level_screen = LevelScreen()
rumble_screen = RumbleScreen()
azimuth_screen = AzimuthScreen()

# Init start up state
main_screen.show_screen(screen)
mode = Mode.MAIN_MENU
main_screen.update(Mode.RPM)
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
    elif new_mode == Mode.AZIMUTH:
        azimuth_screen.show_screen(screen)

    return new_mode


# Main logic loop
while True:
    sensor.update()
    btn_a, btn_b, btn_c = screen.check_buttons()

    if mode == Mode.MAIN_MENU:
        if btn_a:
            main_screen.update(menu_mode.up())
            time.sleep(0.2)
        elif btn_b:
            mode = update_gui(current_mode=mode, new_mode=menu_mode.select())
            time.sleep(0.2)
        elif btn_c:
            main_screen.update(menu_mode.down())
            time.sleep(0.2)

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

        level_data = level_mode.update(sensor.get_acceleration())
        level_screen.update(level_data)

    elif mode == Mode.RUMBLE:
        if btn_a:
            mode = update_gui(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif btn_b:
            rumble_mode.start()
        elif btn_c:
            sensor.set_offset()

        rumble_data = rumble_mode.update(sensor.get_acceleration())
        rumble_screen.update(rumble_mode)

    elif mode == Mode.AZIMUTH:
        if btn_a:
            mode = update_gui(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif btn_b:
            pass
        elif btn_c:
            pass

        azimuth_mode.update()
        azimuth_screen.update()

    time.sleep(0.016)
