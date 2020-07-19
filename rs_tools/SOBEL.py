from rs_tools.utils import install, pix_val_list, convolution, output_to_window
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

    image = pix_val_list(inImage, RGB=True)
    SOBEL_horizontal = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    SOBEL_vertical = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    horizontal_Gaussian = convolution(image, SOBEL_horizontal)
    vertical_Gaussian = convolution(image, SOBEL_vertical)

    output_name = "horizontal"
    output_to_window(output_name, horizontal_Gaussian)
    output_name = "vertical"
    output_to_window(output_name, vertical_Gaussian)

    num_rows = len(image)
    num_cols = len(image[0])
    SOBEL_Gaussian = image[:]

    for row in range(num_rows):
        for col in range(num_cols):
            SOBEL_Gaussian[row][col] = (
                horizontal_Gaussian[row][col] + vertical_Gaussian[row][col]
            ) / 2

    return SOBEL_Gaussian
