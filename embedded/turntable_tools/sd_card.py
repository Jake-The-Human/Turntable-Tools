import board
from busio import SPI

import storage
from digitalio import DigitalInOut
from adafruit_sdcard import SDCard


def setup_sd_card() -> None:
    """Does what the box says sets up the sd card"""

    cs = DigitalInOut(board.SD_CS)
    sd_spi = SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
    sd_card = SDCard(sd_spi, cs)
    vfs = storage.VfsFat(sd_card)
    storage.mount(vfs, "/sd")
