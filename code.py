"""This file is the entry point for the Turntable Tool"""

from time import sleep
import board
from busio import I2C, SPI
from neopixel import NeoPixel

from modules.helper import (
    UpdateGui,
    Mode,
    PixelColor,
    STRINGS,
    HAS_SD_CARD,
    HAS_ADC_CIRCUIT,
    HAS_MEMS_CIRCUIT,
)
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
from modules.azimuth_mode import AzimuthMode
from modules.azimuth_screen import AzimuthScreen


def setup_sd_card():
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
        Mode.RPM: RPMMode(neo_pixel),
        Mode.LEVEL: LevelMode(neo_pixel),
        Mode.RUMBLE: RumbleMode(neo_pixel),
        Mode.CALIBRATE_MEMS: CalibrateMemsMode(neo_pixel),
        "menu": [Mode.RPM, Mode.LEVEL, Mode.RUMBLE, Mode.CALIBRATE_MEMS],
        "sensor": MemsSensor(i2c_bus),
        "screens": {
            Mode.RPM: RPMScreen(),
            Mode.LEVEL: LevelScreen(),
            Mode.RUMBLE: RumbleScreen(),
            Mode.CALIBRATE_MEMS: CalibrateMemsScreen(),
        },
    }
    # Offset are load from the sd card if saved and the sensor is updated
    calibrate_mode = handler[Mode.CALIBRATE_MEMS]
    handler["sensor"].set_offsets(
        calibrate_mode.acceleration_offset,
        calibrate_mode.gyro_offset,
    )
    return handler


def setup_adc_circuit(neo_pixel: NeoPixel) -> dict:
    return {
        Mode.AZIMUTH: AzimuthMode(neo_pixel),
        Mode.NOISE: None,
        Mode.DISTORTION: None,
        "menu": [Mode.AZIMUTH],
        "sensor": None,
        "screens": {
            Mode.AZIMUTH: AzimuthScreen(),
            Mode.NOISE: None,
            Mode.DISTORTION: None,
        },
    }


def build_menu_list(handlers: list[dict]) -> list[int]:
    menu_list: list[int] = []
    for h in handlers:
        if h:
            menu_list += h["menu"]
    menu_list.append(Mode.ABOUT)
    return menu_list


# Setup Feather board
i2c = board.STEMMA_I2C()
pixel = NeoPixel(board.NEOPIXEL, 1)
screen = Display(i2c)

if HAS_SD_CARD:
    setup_sd_card()

# Setup the different tools
mems_handlers: dict = setup_mems_circuit(i2c, pixel) if HAS_MEMS_CIRCUIT else {}
adc_handlers: dict = setup_adc_circuit(pixel) if HAS_ADC_CIRCUIT else {}

# Setup the display logic for the different tools
battery_info = BatteryInfo(i2c)
main_screen = MenuScreen(battery_info, build_menu_list([adc_handlers, mems_handlers]))
about_screen = AboutScreen()

# Init start up state
update_gui = UpdateGui()
update_gui.callback = main_screen.update
main_screen.show_screen(screen)
device_mode = Mode.MAIN_MENU

buttons = Buttons()


def change_mode(current_mode: int, new_mode: int = Mode.MAIN_MENU) -> int:
    """This function handles update the gui's mode"""
    if new_mode == current_mode:
        return current_mode

    if new_mode == Mode.MAIN_MENU:
        main_screen.show_screen(screen)
    elif new_mode == Mode.ABOUT:
        about_screen.show_screen(screen)
    elif new_mode in mems_handlers:
        mems_handlers["screens"][new_mode].show_screen(screen)
    elif new_mode in adc_handlers:
        adc_handlers["screens"][new_mode].show_screen(screen)
    else:
        new_mode = Mode.MAIN_MENU
        main_screen.show_screen(screen)

    return new_mode


# Main logic loop
while True:
    buttons.update()

    if device_mode == Mode.MAIN_MENU:
        if buttons.a_pressed():
            main_screen.up()
        elif buttons.b_pressed():
            device_mode = change_mode(
                current_mode=device_mode, new_mode=main_screen.select()
            )
        elif buttons.c_pressed():
            main_screen.down()

        update_gui.callback = main_screen.update
        pixel.fill(PixelColor.OFF)

    elif device_mode in mems_handlers:
        mems_sensor: MemsSensor = mems_handlers["sensor"]
        mems_mode = mems_handlers[device_mode]
        mems_mode_screen = mems_handlers["screens"][device_mode]

        if buttons.a_pressed():
            device_mode = change_mode(current_mode=device_mode)

        mems_mode.handle_buttons(buttons)

        mems_sensor.update()
        mems_mode.update(mems_sensor)
        update_gui.callback = lambda: mems_mode_screen.update(mems_mode)

    elif device_mode in adc_handlers:
        adc_sensor = mems_handlers["sensor"]
        adc_mode = adc_handlers[device_mode]
        adc_mode_screen = adc_handlers["screens"][device_mode]

        if buttons.a_pressed():
            device_mode = change_mode(current_mode=device_mode)

        adc_mode.update()
        update_gui.callback = lambda: adc_mode_screen.update(adc_mode)

    elif device_mode == Mode.ABOUT:
        if buttons.a_pressed():
            device_mode = change_mode(current_mode=device_mode)

    update_gui.update()
    sleep(0.015)
