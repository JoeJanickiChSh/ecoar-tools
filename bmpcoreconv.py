'''
BMPCORE Bitmap Converter

Written by Joe Janicki
2026-11-23

Convert arbitrary image files to 32-bit per pixel
bitmap image in the simplest format using the
12-byte BMPCOREHEADER header.

Specify an input and output file.
'''
import sys

if len(sys.argv) < 2:
    print("Error: no input file specified")
    quit()
if len(sys.argv) < 3:
    print("Error: no output file specified")
    quit()

import pygame as pg
pg.init()

srf = pg.image.load(sys.argv[1])

pixdata = bytearray(4 * srf.get_width() * srf.get_height())
for y in range(srf.get_height()):
    for x in range(srf.get_width()):
        clr = srf.get_at((x,srf.get_height() - 1 - y))
        r,g,b = clr[:3]
        pixdata[(y * srf.get_width() + x) * 4] = b
        pixdata[(y * srf.get_width() + x) * 4 + 1] = g
        pixdata[(y * srf.get_width() + x) * 4 + 2] = r
        pixdata[(y * srf.get_width() + x) * 4 + 3] = 255
    print(f"\r{round(100 * y / srf.get_height(), 2)}%", end='')

pixdata = bytes(pixdata)
header = b'BM'
# File Size
header += (26 + len(pixdata)).to_bytes(4, 'little')
# Reserved
header += (0).to_bytes(4, 'little')

# Pixel data offset
header += (26).to_bytes(4, 'little')

# Header size
header += (12).to_bytes(4, 'little')
header += srf.get_width().to_bytes(2, 'little')
header += srf.get_height().to_bytes(2, 'little')
header += (1).to_bytes(2, 'little')
header += (32).to_bytes(2, 'little')

with open(sys.argv[2], "wb") as fp:
    fp.write(header + pixdata)
