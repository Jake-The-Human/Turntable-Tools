"""This file is the entry point for the Turntable Tool"""

import time
import board

import neopixel

# import busio
# import digitalio
# import storage
# import adafruit_sdcard

from modules.helper import Mode, RPM_TEST_LEN, RPM_TEST_START_UP_TIME
from modules.display import Display
from modules.mems_sensor import MemsSensor
from modules.rpm_mode import RPMMode
from modules.level_mode import Leveling
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

i2c = board.STEMMA_I2C()
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 1.0

rpm_mode = RPMMode()
level_mode = Leveling()

sensor = MemsSensor(i2c)
screen = Display(board.I2C())

main_screen = MainScreen()
rpm_screen = RPMScreen()
level_screen = LevelScreen()
rumble_screen = RumbleScreen()

main_screen.show_screen(screen)

tool_mode = Mode.MAIN_MENU

timer: float = 0

# TODO REMOVE SLEEPS just check time or something

while True:
    sensor.update()

    btn_a, btn_b, btn_c = screen.check_buttons()

    if tool_mode == Mode.MAIN_MENU:
        if btn_a:
            tool_mode = Mode.RPM
            rpm_screen.show_screen(screen)
            time.sleep(2)
            sensor.set_offset()

        if btn_b:
            tool_mode = Mode.LEVEL
            level_screen.show_screen(screen)
            time.sleep(1)

        if btn_c:
            tool_mode = Mode.RUMBLE
            rumble_screen.show_screen(screen)
            time.sleep(2)
            sensor.set_offset()
        pixel.fill((0, 0, 0))

    elif tool_mode == Mode.RPM:
        if btn_a:
            tool_mode = Mode.MAIN_MENU
            main_screen.show_screen(screen)
            time.sleep(0.2)

        if btn_b:
            # Start recording data for wow and flutter
            pixel.fill((255, 255, 0))
            sensor.set_offset()
            rpm_mode.start()
            rpm_screen.start_recording_data(RPM_TEST_START_UP_TIME)
            timer = time.time()
            pixel.fill((0, 255, 0))

        if btn_c:
            # set rpm
            pass

        if rpm_mode.is_recording_data() and (time.time() - timer) >= RPM_TEST_LEN:
            rpm_screen.stop_recording_data(rpm_mode.stop())
            pixel.fill((255, 0, 0))
            sensor.reset_offset()

        new_rpm = rpm_mode.update(sensor.get_rpm())
        rpm_screen.update(new_rpm)

    elif tool_mode == Mode.LEVEL:
        if btn_a:
            tool_mode = Mode.MAIN_MENU
            main_screen.show_screen(screen)
            time.sleep(0.2)

        if btn_b:
            pass

        if btn_c:
            sensor.set_offset()

        x, y, _ = sensor.get_acceleration()
        new_x, new_y = level_mode.update(x, y)
        level_screen.update(new_x, new_y)

    elif tool_mode == Mode.RUMBLE:
        if btn_a:
            tool_mode = Mode.MAIN_MENU
            main_screen.show_screen(screen)
            time.sleep(0.2)

        if btn_b:
            pass

        if btn_c:
            sensor.set_offset()

    time.sleep(0.016)
