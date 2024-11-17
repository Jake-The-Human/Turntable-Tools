"""This file is the entry point for the Turntable Tool"""

import time
import board
import neopixel

from modules.helper import (
    UpdateGui,
    Mode,
    PixelColor,
    HAS_SD_CARD,
    HAS_ADC_CIRCUIT,
    HAS_MEMS_CIRCUIT,
)
from modules.display import Display
from modules.mems_sensor import MemsSensor
from modules.buttons import Buttons
from modules.rpm_mode import RPMMode
from modules.level_mode import LevelMode
from modules.rumble_mode import RumbleMode
from modules.calibrate_mode import CalibrateMode
from modules.azimuth_mode import AzimuthMode
from modules.menu_screen import MenuScreen
from modules.rpm_screen import RPMScreen
from modules.level_screen import LevelScreen
from modules.rumble_screen import RumbleScreen
from modules.azimuth_screen import AzimuthScreen
from modules.calibrate_screen import CalibrateScreen
from modules.about_screen import AboutScreen

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
buttons = Buttons()

# Setup the different tools
if HAS_MEMS_CIRCUIT:
    rpm_mode = RPMMode(pixel)
    level_mode = LevelMode(pixel)
    rumble_mode = RumbleMode(pixel)
    rpm_screen = RPMScreen()
    level_screen = LevelScreen()
    rumble_screen = RumbleScreen()

if HAS_ADC_CIRCUIT:
    azimuth_mode = AzimuthMode(pixel)
    azimuth_screen = AzimuthScreen()

# Setup the display logic for the different tools
main_screen = MenuScreen()
calibrate_screen = CalibrateScreen(sensor.calibrate_mode)
about_screen = AboutScreen()

# Init start up state
update_gui = UpdateGui()
update_gui.callback = main_screen.update
main_screen.show_screen(screen)
mode = Mode.MAIN_MENU


def change_mode(current_mode: int, new_mode: int) -> int:
    """This function handles update the gui's mode"""
    if new_mode == current_mode:
        return current_mode

    if new_mode == Mode.MAIN_MENU:
        main_screen.show_screen(screen)
    elif new_mode == Mode.RPM and HAS_MEMS_CIRCUIT:
        rpm_screen.show_screen(screen)
    elif new_mode == Mode.LEVEL and HAS_MEMS_CIRCUIT:
        level_screen.show_screen(screen)
    elif new_mode == Mode.RUMBLE and HAS_MEMS_CIRCUIT:
        rumble_screen.show_screen(screen)
    elif new_mode == Mode.AZIMUTH and HAS_ADC_CIRCUIT:
        azimuth_screen.show_screen(screen)
    elif new_mode == Mode.CALIBRATE:
        calibrate_screen.show_screen(screen)
    elif new_mode == Mode.ABOUT:
        about_screen.show_screen(screen)
    else:
        new_mode = Mode.MAIN_MENU
        main_screen.show_screen(screen)

    return new_mode


# Main logic loop
while True:
    buttons.update()
    sensor.update()

    if mode == Mode.MAIN_MENU:
        if buttons.a_pressed():
            main_screen.up()
        elif buttons.b_pressed():
            mode = change_mode(current_mode=mode, new_mode=main_screen.select())
        elif buttons.c_pressed():
            main_screen.down()

        update_gui.callback = main_screen.update
        pixel.fill(PixelColor.OFF)

    elif mode == Mode.RPM and HAS_MEMS_CIRCUIT:
        if buttons.a_pressed():
            mode = change_mode(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif buttons.b_pressed():
            # Start recording rpm data
            rpm_mode.start()
        # elif buttons.c_pressed():
        #     # This sleep is used to avoided capturing the button press
        #     time.sleep(0.7)
        #     sensor.set_offset()

        new_rpm = rpm_mode.update(sensor.get_rpm())
        update_gui.callback = lambda: rpm_screen.update(rpm_mode, new_rpm)

    elif mode == Mode.LEVEL and HAS_MEMS_CIRCUIT:
        if buttons.a_pressed():
            mode = change_mode(current_mode=mode, new_mode=Mode.MAIN_MENU)

        level_data = level_mode.update(sensor.get_acceleration())
        update_gui.callback = lambda: level_screen.update(level_data)

    elif mode == Mode.RUMBLE and HAS_MEMS_CIRCUIT:
        if buttons.a_pressed():
            mode = change_mode(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif buttons.b_pressed():
            rumble_mode.start()

        rumble_data = rumble_mode.update(sensor.get_acceleration())
        update_gui.callback = lambda: rumble_screen.update(rumble_mode)

    elif mode == Mode.AZIMUTH and HAS_ADC_CIRCUIT:
        if buttons.a_pressed():
            mode = change_mode(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif buttons.b_pressed():
            pass
        elif buttons.c_pressed():
            pass

        azimuth_mode.update()
        update_gui.callback = azimuth_screen.update

    elif mode == Mode.CALIBRATE:
        if buttons.a_pressed():
            mode = change_mode(current_mode=mode, new_mode=Mode.MAIN_MENU)
        elif buttons.b_pressed():
            sensor.calibrate_mode.start(pixel)

        sensor.calibrate_mode.update(pixel, sensor.acceleration, sensor.gyro)
        update_gui.callback = lambda: calibrate_screen.update(sensor.calibrate_mode)

    elif mode == Mode.ABOUT:
        if buttons.a_pressed():
            mode = change_mode(current_mode=mode, new_mode=Mode.MAIN_MENU)

    update_gui.update()
    time.sleep(0.015)
