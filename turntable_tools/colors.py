"""This file holds all the colors"""

from displayio import Palette

# Colors for the display
DISPLAY_BLACK: int = 0x000000
DISPLAY_WHITE: int = 0xFFFFFF


# Colors for NeoPixel
NEO_PIXEL_OFF: tuple = (0, 0, 0)
NEO_PIXEL_GREEN: tuple = (0, 255, 0)
NEO_PIXEL_YELLOW: tuple = (255, 255, 0)
NEO_PIXEL_RED: tuple = (255, 0, 0)


# Black and white color palettes
PALETTE_BLACK = Palette(1)
PALETTE_BLACK[0] = DISPLAY_BLACK
PALETTE_WHITE = Palette(1)
PALETTE_WHITE[0] = DISPLAY_WHITE
