from rs_tools.utils import install, pix_val_list, convolution, output_to_window

install()

import numpy
import sys
from PIL import Image, ImageFile, ImageDraw


def generate_SOBEL(inFile):
    try:
        inImage = Image.open(inFile, "r")
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    image = pix_val_list(inImage, RGB=False)
    SOBEL_horizontal_left = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    SOBEL_horizontal_right = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    SOBEL_vertical_bottom = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    SOBEL_vertical_top = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    horizontal_Gaussian_left = convolution(image, SOBEL_horizontal_left)
    horizontal_Gaussian_right = convolution(image, SOBEL_horizontal_right)
    vertical_Gaussian_bottom = convolution(image, SOBEL_vertical_bottom)
    vertical_Gaussian_top = convolution(image, SOBEL_vertical_top)

    num_rows = len(image)
    num_cols = len(image[0])
    SOBEL_Gaussian = image[:]

    for row in range(num_rows):
        for col in range(num_cols):
            SOBEL_Gaussian[row][col] = (
                horizontal_Gaussian_left[row][col]
                + horizontal_Gaussian_left[row][col]
                + vertical_Gaussian_bottom[row][col]
                + vertical_Gaussian_top[row][col]
            )

    return SOBEL_Gaussian
