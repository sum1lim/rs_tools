from rs_tools.utils import install, pix_val_extractor
import sys
import re
import os

install()
import numpy
from PIL import Image, ImageFile, ImageDraw


def generate_SOBEL(inFile):
    try:
        inImage = Image.open(inFile, "r")
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    pix_val_li = pix_val_extractor(inImage, BlackAndWhite=True)

    SOBEL_horizontal = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

    SOBEL_vertical = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
