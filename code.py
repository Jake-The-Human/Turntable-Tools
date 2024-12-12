"""This file is the entry point for the Turntable Tool"""

from time import sleep
import board
from busio import I2C, SPI
from neopixel import NeoPixel

import modules.mode as MODE
import modules.colors as COLORS
from modules.helper import (
    HAS_SD_CARD,
    HAS_ADC_CIRCUIT,
    HAS_MEMS_CIRCUIT,
)
from modules.update_gui import UpdateGui
from modules.display import Display
from modules.buttons import Buttons
from modules.menu_screen import MenuScreen
from modules.about_screen import AboutScreen
from modules.battery_info import BatteryInfo

# MEMS imports
from modules.mems_sensor import MemsSensor
from modules.calibrate_mems_mode import CalibrateMemsMode
from modules.rpm_mode import RPMMode
from modules.level_mode import LevelMode
from modules.rumble_mode import RumbleMode
from modules.rpm_screen import RPMScreen
from modules.level_screen import LevelScreen
from modules.rumble_screen import RumbleScreen
from modules.calibrate_mems_screen import CalibrateMemsScreen

# ADC imports
from modules.adc_sensor import AdcSensor
from modules.azimuth_mode import AzimuthMode
from modules.azimuth_screen import AzimuthScreen


def setup_sd_card() -> None:
    import storage
    from digitalio import DigitalInOut
    from adafruit_sdcard import SDCard

    cs = DigitalInOut(board.SD_CS)
    sd_spi = SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
    sd_card = SDCard(sd_spi, cs)
    vfs = storage.VfsFat(sd_card)
    storage.mount(vfs, "/sd")


def setup_mems_circuit(i2c_bus: I2C, neo_pixel: NeoPixel) -> dict:
    handler = {
        MODE.RPM: RPMMode(neo_pixel),
        MODE.LEVEL: LevelMode(neo_pixel),
        MODE.RUMBLE: RumbleMode(neo_pixel),
        MODE.CALIBRATE_MEMS: CalibrateMemsMode(neo_pixel),
        "menu": [MODE.RPM, MODE.LEVEL, MODE.RUMBLE, MODE.CALIBRATE_MEMS],
        "sensor": MemsSensor(i2c_bus),
        "screens": {
            MODE.RPM: RPMScreen(),
            MODE.LEVEL: LevelScreen(),
            MODE.RUMBLE: RumbleScreen(),
            MODE.CALIBRATE_MEMS: CalibrateMemsScreen(),
        },
    }
    # Offset are load from the sd card if saved and the sensor is updated
    calibrate_mode = handler[MODE.CALIBRATE_MEMS]
    handler["sensor"].set_offsets(
        calibrate_mode.acceleration_offset,
        calibrate_mode.gyro_offset,
    )
    return handler


def setup_adc_circuit(_: I2C, neo_pixel: NeoPixel) -> dict:
    return {
        MODE.AZIMUTH: AzimuthMode(neo_pixel),
        "menu": [MODE.AZIMUTH],
        "sensor": AdcSensor(),
        "screens": {
            MODE.AZIMUTH: AzimuthScreen(),
        },
    }


def build_menu_list(handlers: list[dict]) -> list[int]:
    menu_list: list[int] = []
    for handler in handlers:
        if handler:
            menu_list += handler["menu"]
    menu_list.append(MODE.ABOUT)
    return menu_list


# Setup Feather board
i2c = board.STEMMA_I2C()
pixel = NeoPixel(board.NEOPIXEL, n=1)
screen = Display(i2c)

if HAS_SD_CARD:
    setup_sd_card()

# Setup the different tools
mems_handlers: dict = setup_mems_circuit(i2c, pixel) if HAS_MEMS_CIRCUIT else {}
adc_handlers: dict = setup_adc_circuit(i2c, pixel) if HAS_ADC_CIRCUIT else {}

# Setup the display logic for the different tools
battery_info = BatteryInfo(i2c)
main_screen = MenuScreen(battery_info, build_menu_list([mems_handlers, adc_handlers]))
about_screen = AboutScreen()

# Init start up state
update_gui = UpdateGui()
update_gui.callback = main_screen.update
screen.set_display(main_screen)
device_mode = MODE.MAIN_MENU

# Init the input devices
buttons = Buttons()


def change_mode(current_mode: int, new_mode: int = MODE.MAIN_MENU) -> int:
    """This function handles update the gui's mode"""
    if new_mode == current_mode:
        return current_mode

    if new_mode == MODE.MAIN_MENU:
        screen.set_display(main_screen)
    elif new_mode == MODE.ABOUT:
        screen.set_display(about_screen)
    elif new_mode in mems_handlers:
        screen.set_display(mems_handlers["screens"][new_mode])
    elif new_mode in adc_handlers:
        screen.set_display(adc_handlers["screens"][new_mode])
    else:
        new_mode = MODE.MAIN_MENU
        screen.set_display(main_screen)

    return new_mode


# trying to remove static when starting the device
while not screen.display.is_awake:
    continue


# Main logic loop
while True:
    buttons.update()

    if device_mode == MODE.MAIN_MENU:
        if buttons.a_pressed():
            main_screen.up()
        elif buttons.b_pressed():
            device_mode = change_mode(
                current_mode=device_mode, new_mode=main_screen.select()
            )
        elif buttons.c_pressed():
            main_screen.down()

        update_gui.callback = main_screen.update
        pixel.fill(COLORS.NEO_PIXEL_OFF)

    elif device_mode in mems_handlers:
        mems_sensor: MemsSensor = mems_handlers["sensor"]
        mems_mode = mems_handlers[device_mode]
        mems_mode_screen = mems_handlers["screens"][device_mode]

        if buttons.a_pressed():
            device_mode = change_mode(current_mode=device_mode)
            mems_sensor.clear()

        mems_mode.handle_buttons(buttons)

        mems_sensor.update()
        mems_mode.update(mems_sensor)
        update_gui.callback = lambda: mems_mode_screen.update(mems_mode)

    elif device_mode in adc_handlers:
        adc_sensor: AdcSensor = adc_handlers["sensor"]
        adc_mode = adc_handlers[device_mode]
        adc_mode_screen = adc_handlers["screens"][device_mode]

        if buttons.a_pressed():
            device_mode = change_mode(current_mode=device_mode)
            adc_sensor.clear()

        adc_mode.handle_buttons(buttons)

        adc_sensor.update()
        adc_mode.update(adc_sensor)
        update_gui.callback = lambda: adc_mode_screen.update(adc_mode)

    elif device_mode == MODE.ABOUT:
        if buttons.a_pressed():
            device_mode = change_mode(current_mode=device_mode)

    update_gui.update()
    # sleep(0.015)
